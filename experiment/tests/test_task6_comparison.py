import ast
import contextlib
import copy
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from task6_comparison import (DEFAULT_CONFIG, MODES, citation_audit, execute,
                             export_review, load_inputs, messages_for, fit_messages,
                             prepare_plan, read_json, summarize, validate_run, write_csv)


class CharacterTokenizer:
    def apply_chat_template(self,messages,**kwargs):
        return list(''.join(m['content'] for m in messages))


class Task6Tests(unittest.TestCase):
    def setUp(self):
        self.captured_stdout = contextlib.redirect_stdout(io.StringIO())
        self.captured_stdout.__enter__()
        self.addCleanup(self.captured_stdout.__exit__,None,None,None)

    @classmethod
    def setUpClass(cls):
        cls.plan = prepare_plan(ROOT)
        cls.chunks, cls.questions = load_inputs(ROOT/'data',cls.plan)

    def generate_fixture(self,messages):
        return dict(answer='Đáp án kiểm thử, không phải output LLM.',input_tokens=100,
                    output_tokens=20,seconds=.1,reached_token_limit=False)

    def config_fixture(self):
        return dict(DEFAULT_CONFIG,max_input_tokens=200000)

    def test_plan_uses_real_top5_from_each_method_and_checks_data(self):
        self.assertEqual(len(self.plan['rankings']),20)
        for modes in self.plan['rankings'].values():
            self.assertEqual(set(modes),set(MODES[1:]))
            self.assertTrue(all(len(ids)==5 and len(set(ids))==5 for ids in modes.values()))
        changed = copy.deepcopy(self.plan)
        changed['data_sha256']['corpus'] = 'wrong'
        with self.assertRaisesRegex(ValueError,'checksum'):
            load_inputs(ROOT/'data',changed)

    def test_equal_system_prompts_no_reference_or_answer_in_prompt(self):
        q = self.questions[0]
        baseline = messages_for(q['question'],[])
        rag = messages_for(q['question'],self.chunks[:1])
        self.assertEqual(baseline[0],rag[0])
        self.assertEqual(len(baseline),2)
        self.assertEqual(len(rag),2)
        self.assertIn(q['question'],baseline[1]['content'])
        self.assertNotIn(q['reference_answer'],baseline[1]['content'])
        self.assertNotIn(self.chunks[0]['text'],baseline[1]['content'])
        self.assertIn(self.chunks[0]['text'],rag[1]['content'])

    def test_budget_drops_whole_trailing_chunks_and_never_empty_rag(self):
        tokenizer = CharacterTokenizer()
        question = 'Ví dụ'
        hits = self.chunks[:2]
        budget = len(tokenizer.apply_chat_template(messages_for(question,hits[:1])))
        config = dict(DEFAULT_CONFIG,max_input_tokens=budget)
        _,used,omitted = fit_messages(tokenizer,question,hits,config)
        self.assertEqual(used,hits[:1])
        self.assertEqual(omitted,hits[1:])
        with self.assertRaises(ValueError):
            fit_messages(tokenizer,question,hits,dict(config,max_input_tokens=1))

    def test_all_80_conditions_checkpoint_resume_and_config_mismatch(self):
        calls = []
        def generate(messages):
            calls.append(messages)
            return self.generate_fixture(messages)
        with tempfile.TemporaryDirectory() as directory:
            run = execute(self.chunks,self.questions,self.plan,directory,self.config_fixture(),
                          CharacterTokenizer(),generate)
            self.assertEqual(len(calls),80)
            self.assertTrue(all(len(m)==2 for m in calls))
            self.assertEqual(len(run['questions']),20)
            self.assertEqual(sum(len(q['answers']) for q in run['questions']),80)
            validate_run(run)
            execute(self.chunks,self.questions,self.plan,directory,self.config_fixture(),
                    CharacterTokenizer(),generate)
            self.assertEqual(len(calls),80)
            with self.assertRaisesRegex(ValueError,'different run'):
                execute(self.chunks,self.questions,self.plan,directory,
                        dict(self.config_fixture(),max_new_tokens=100),CharacterTokenizer(),generate)

    def test_partial_run_resumes_without_repeating_completed_answer(self):
        state = {'calls':0}
        def interrupted(messages):
            state['calls']+=1
            if state['calls']==2:
                raise RuntimeError('simulated interruption')
            return self.generate_fixture(messages)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(RuntimeError):
                execute(self.chunks,self.questions[:1],self.plan,directory,self.config_fixture(),
                        CharacterTokenizer(),interrupted)
            partial = read_json(Path(directory)/'answers_comparison.json')
            self.assertEqual(len(partial['questions'][0]['answers']),1)
            count = []
            def continued(messages):
                count.append(1)
                return self.generate_fixture(messages)
            execute(self.chunks,self.questions[:1],self.plan,directory,self.config_fixture(),
                    CharacterTokenizer(),continued)
            self.assertEqual(len(count),3)

    def test_unscored_output_has_no_invented_accuracy_and_scores_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            run = execute(self.chunks,self.questions[:1],self.plan,directory,self.config_fixture(),
                          CharacterTokenizer(),self.generate_fixture)
            export_review(run,directory)
            with self.assertRaisesRegex(ValueError,'Review incomplete'):
                summarize(directory)
            path = Path(directory)/'manual_review.csv'
            with path.open(encoding='utf-8-sig',newline='') as handle:
                rows = list(csv.DictReader(handle))
            for row in rows:
                row.update(answered='yes',correctness='2',completeness='2',unsupported_claim='0',
                           citation_support='na' if row['mode']=='baseline' else '2',
                           reviewer='test_fixture',notes='Synthetic unit-test scores, not actual evaluation.')
            write_csv(path,rows)
            before = path.read_bytes()
            export_review(run,directory)
            self.assertEqual(before,path.read_bytes())
            summary = summarize(directory)
            self.assertTrue(all(row['accuracy']==1 for row in summary))
            self.assertEqual(summary[0]['fully_supported_citation_rate'],'NA')
            changed = copy.deepcopy(run)
            changed['questions'][0]['answers']['baseline']['answer']+=' changed'
            with self.assertRaisesRegex(ValueError,'different answers'):
                export_review(changed,directory)

    def test_citations_are_syntactic_only_and_no_baseline_sources(self):
        self.assertTrue(citation_audit('Đúng [a]',[dict(chunk_id='a')])['has_valid_citation'])
        self.assertEqual(citation_audit('Sai [invented]',[])['unknown_ids'],['invented'])

    def test_paired_comparison_counts_improvements_and_regressions(self):
        with tempfile.TemporaryDirectory() as directory:
            run = execute(self.chunks,self.questions[:2],self.plan,directory,self.config_fixture(),
                          CharacterTokenizer(),self.generate_fixture)
            export_review(run,directory)
            path = Path(directory)/'manual_review.csv'
            with path.open(encoding='utf-8-sig',newline='') as handle:
                rows = list(csv.DictReader(handle))
            for row in rows:
                correct = row['question_id']=='Q02'
                if row['mode']=='tfidf':
                    correct = not correct
                elif row['mode']=='embedding':
                    correct = True
                row.update(answered='yes',correctness='2' if correct else '0',completeness='2',
                           unsupported_claim='0' if correct else '1',
                           citation_support='na' if row['mode']=='baseline' else '2',
                           reviewer='test_fixture',notes='Synthetic unit-test scores only.')
            write_csv(path,rows)
            summary = {r['mode']:r for r in summarize(directory)}
            self.assertEqual(summary['tfidf']['corrected_vs_baseline'],1)
            self.assertEqual(summary['tfidf']['regressed_vs_baseline'],1)
            self.assertEqual(summary['tfidf']['delta_accuracy_vs_baseline'],0)
            self.assertEqual(summary['embedding']['delta_accuracy_vs_baseline'],.5)

    def test_notebook_is_python_and_frozen_plan_matches_current_inputs(self):
        notebook = read_json(ROOT/'notebooks/S07_Task6_RAG_Comparison.ipynb')
        for cell in notebook['cells']:
            if cell['cell_type']=='code' and not cell['source'].startswith('%'):
                ast.parse(cell['source'])
        plan_cell = next(c['source'] for c in notebook['cells'] if c['source'].startswith('import json\nFROZEN_PLAN'))
        namespace = {}
        exec(plan_cell,namespace)
        self.assertEqual(namespace['FROZEN_PLAN'],self.plan)

    def test_notebook_smoke_executes_end_to_end_with_mock_model(self):
        # Execute actual notebook cells, but never download/run a model in tests.
        notebook = read_json(ROOT/'notebooks/S07_Task6_RAG_Comparison.ipynb')
        fake_torch = types.ModuleType('torch')
        fake_torch.cuda = types.SimpleNamespace(is_available=lambda:True,
                                                get_device_name=lambda _: 'mock_gpu',empty_cache=lambda:None)
        fake_display = types.ModuleType('IPython.display')
        fake_display.display = lambda *_:None
        fake_display.Markdown = lambda value:value
        fake_display.FileLink = lambda value:value
        modules = {'torch':fake_torch,'IPython':types.ModuleType('IPython'),'IPython.display':fake_display}
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules,modules), patch('importlib.metadata.version',return_value='mock-version'):
            namespace = {'__name__':'notebook_test'}
            for cell in notebook['cells']:
                if cell['cell_type']!='code' or cell['source'].startswith('%'):
                    continue
                source = cell['source']
                if 'DATA_ROOT = None' in source:
                    source = source.replace('DATA_ROOT = None',f'DATA_ROOT = Path({str(ROOT / "data")!r})')
                    source = source.replace("Path('/kaggle/working/s07_task6_4way')",f'Path({str(Path(directory)/"run")!r})')
                    source = source.replace('EVAL_LIMIT = None','EVAL_LIMIT = 2')
                if 'tokenizer, generate = load_generator(CONFIG)' in source:
                    namespace['load_generator'] = lambda _: (CharacterTokenizer(),self.generate_fixture)
                exec(compile(source,'task6_notebook_cell','exec'),namespace)
            output = Path(directory)/'run'
            manifest = read_json(output/'run_manifest.json')
            self.assertEqual(manifest['completed_answers'],8)
            self.assertEqual(manifest['generation_status'],'completed')
            self.assertTrue((Path(directory)/'run_results.zip').exists())
            with (output/'manual_review.csv').open(encoding='utf-8-sig',newline='') as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows),8)
            self.assertTrue(all(row['correctness']=='' for row in rows))


if __name__=='__main__':
    unittest.main()
