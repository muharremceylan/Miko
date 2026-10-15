import curriculum from '../../../../akademi_ai_prototip/content/kpss/lisans/matematik/curriculum.json' with { type: 'json' };
import { bank, contentReady } from './content.js';

export { curriculum, bank };
export const STORAGE_KEY = 'akademi_math_v1_kpss_lisans';
export const nodes = new Map(curriculum.topics.map(t => [t.id, t]));
export const leaves = curriculum.topics.filter(t => !t.children.length);
export const tabs = ['lesson', 'summary', 'formulas', 'examples', 'test', 'audio', 'ai'];
const fresh = () => ({ version: 1, curriculumVersion: curriculum.version, topics: {}, lastTopic: null, attempts: [], activeAttempt: null });
const object = v => v !== null && typeof v === 'object' && !Array.isArray(v);
const time = n => Number.isFinite(n) && n > 0;
export function validQuestion(q) {
  return object(q) && typeof q.id === 'string' && Number.isSafeInteger(q.version) && q.version > 0 && nodes.has(q.topicId) &&
    typeof q.text === 'string' && q.text.length > 0 && Array.isArray(q.options) && q.options.length === 5 &&
    q.options.every(o => typeof o === 'string') && new Set(q.options).size === 5 && Number.isInteger(q.answer) && q.answer >= 0 && q.answer < 5 &&
    Array.isArray(q.steps) && q.steps.length > 0 && q.steps.every(s => typeof s === 'string') && typeof q.formula === 'string';
}
export function validState(s) {
  if (!object(s) || s.version !== 1 || s.curriculumVersion !== curriculum.version || !object(s.topics) ||
      !(s.lastTopic === null || nodes.has(s.lastTopic)) || !Array.isArray(s.attempts)) return false;
  if (!Object.entries(s.topics).every(([id, p]) => nodes.has(id) && object(p) && typeof p.completed === 'boolean' && (!p.completed || contentReady(id)) &&
      tabs.includes(p.tab) && object(p.scroll) && Object.entries(p.scroll).every(([tab, y]) => tabs.includes(tab) && Number.isFinite(y) && y >= 0))) return false;
  if (!s.attempts.every(a => object(a) && typeof a.id === 'string' && nodes.has(a.topicId) && ['learn','assessment'].includes(a.mode) &&
      time(a.startedAt) && (a.finishedAt === null || (time(a.finishedAt) && a.finishedAt >= a.startedAt)) &&
      Array.isArray(a.questions) && a.questions.length > 0 && a.questions.length <= 30 && a.questions.every(validQuestion) &&
      new Set(a.questions.map(q => q.id)).size === a.questions.length &&
      a.questions.every(q => descendantIds(a.topicId).includes(q.topicId)) &&
      Array.isArray(a.answers) && a.answers.length === a.questions.length &&
      a.answers.every(v => v === null || (object(v) && time(v.at) && (v.choice === null || (Number.isInteger(v.choice) && v.choice >= 0 && v.choice < 5)))) &&
      Number.isInteger(a.current) && a.current >= 0 && a.current < a.questions.length)) return false;
  return new Set(s.attempts.map(a => a.id)).size === s.attempts.length &&
    (s.activeAttempt === null || s.attempts.some(a => a.id === s.activeAttempt && !a.finishedAt));
}
export function descendantIds(id) {
  const topic = nodes.get(id); return topic ? [id, ...topic.children.flatMap(descendantIds)] : [];
}
export function latestAnswers(attempts) {
  const latest = new Map();
  for (const attempt of attempts) attempt.answers.forEach((answer, i) => {
    if (!answer || answer.choice === null) return;
    const q = attempt.questions[i], key = q.id + ':' + q.version;
    if (!latest.has(key) || latest.get(key).at <= answer.at) latest.set(key, { at: answer.at, correct: answer.choice === q.answer, question:q, choice:answer.choice, attemptId:attempt.id });
  });
  return latest;
}
// Defter yalnız biten testlerin cevaplarını gösterir; değerlendirme sırasında çözüm açılmaz.
export function mistakes(attempts, topicId = null) {
  const ids = topicId ? descendantIds(topicId) : null;
  return [...latestAnswers(attempts.filter(a => a.finishedAt !== null)).values()]
    .filter(v => !v.correct && (!ids || ids.includes(v.question.topicId)))
    .sort((a,b) => b.at - a.at);
}
export function eligibleQuestions(topicId, filter, attempts) {
  const ids = descendantIds(topicId), latest = latestAnswers(attempts);
  return bank.filter(q => ids.includes(q.topicId)).filter(q => {
    const answer = latest.get(q.id + ':' + q.version);
    return filter === 'wrong' ? !!answer && !answer.correct : filter === 'unseen' ? !answer : filter === 'all';
  });
}
export function selectQuestions(pool, count, random = Math.random) {
  if (!Number.isInteger(count) || count < 1 || count > 30 || count > pool.length) throw new Error('insufficient-pool');
  const copy = [...pool];
  for (let i = copy.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [copy[i], copy[j]] = [copy[j], copy[i]]; }
  return structuredClone(copy.slice(0, count));
}
export function attemptSummary(a) {
  let solved = 0, correct = 0;
  a.answers.forEach((answer, i) => { if (answer && answer.choice !== null) { solved++; if (answer.choice === a.questions[i].answer) correct++; } });
  return { total: a.questions.length, solved, correct, wrong: solved - correct, blank: a.questions.length - solved,
    rate: solved ? Math.round(100 * correct / solved) : null, elapsedMs: Math.max(0, (a.finishedAt ?? Date.now()) - a.startedAt) };
}
export class MathProgress {
  constructor(storage) {
    this.storage = storage; this.notice = ''; this.state = fresh();
    try { const raw = storage.getItem(STORAGE_KEY); if (raw !== null) { const saved = JSON.parse(raw); if (!validState(saved)) throw new Error('invalid'); this.state = saved; } }
    catch { this.notice = 'Matematik kaydı okunamadı. Bu oturumda çalışabilirsin; önceki kayıt yeni çalışma kaydedilene kadar değiştirilmez.'; }
  }
  save() {
    try { this.storage.setItem(STORAGE_KEY, JSON.stringify(this.state)); this.notice = ''; return true; }
    catch { this.notice = 'Matematik ilerlemesi kaydedilemedi. Çalışman bu oturumda sürer; sayfa kapanınca yeni kayıtlar kaybolabilir.'; return false; }
  }
  touch(id, tab, y = 0) {
    if (!nodes.has(id) || !tabs.includes(tab)) return;
    const p = this.state.topics[id] ?? { completed: false, tab, scroll: {} };
    p.tab = tab; p.scroll[tab] = Math.max(0, y); this.state.topics[id] = p; this.state.lastTopic = id; this.save();
  }
  complete(id, value) {
    if (!contentReady(id) || typeof value !== 'boolean') return;
    this.touch(id, this.state.topics[id]?.tab ?? 'lesson'); this.state.topics[id].completed = value; this.save();
  }
  start(topicId, filter, count, mode = 'learn') {
    if (!['learn','assessment'].includes(mode)) throw new Error('invalid-mode');
    if (this.active()) throw new Error('active-attempt');
    const questions = selectQuestions(eligibleQuestions(topicId, filter, this.state.attempts), count);
    return this.createAttempt(topicId, questions, mode);
  }
  review(questionId, version) {
    if(this.active()) throw new Error('active-attempt');
    const item = mistakes(this.state.attempts).find(v => v.question.id === questionId && v.question.version === version);
    if(!item) throw new Error('missing-mistake');
    return this.createAttempt(item.question.topicId, [structuredClone(item.question)], 'learn');
  }
  createAttempt(topicId, questions, mode) {
    const a = { id: globalThis.crypto?.randomUUID?.() ?? Date.now() + '-' + Math.random().toString(36).slice(2),
      topicId, mode, questions, answers: questions.map(() => null), current: 0, startedAt: Date.now(), finishedAt: null };
    this.state.attempts.push(a); this.state.activeAttempt = a.id; this.save(); return a;
  }
  active() { return this.state.attempts.find(a => a.id === this.state.activeAttempt && !a.finishedAt) ?? null; }
  answer(choice) {
    const a = this.active();
    if (!a || a.answers[a.current] !== null || !(choice === null || (Number.isInteger(choice) && choice >= 0 && choice < 5))) return false;
    a.answers[a.current] = { choice, at: Date.now() }; this.save(); return true;
  }
  next() {
    const a = this.active(); if (!a || a.answers[a.current] === null) return false;
    if (a.current + 1 < a.questions.length) a.current++; else return this.finish();
    this.save(); return true;
  }
  finish() {
    const a = this.active(); if (!a) return false;
    a.finishedAt = Math.max(Date.now(), a.startedAt); this.state.activeAttempt = null; this.save(); return a;
  }
  clearAttempts() { this.state.attempts = []; this.state.activeAttempt = null; this.save(); }
  stats(date = null) {
    let solved = 0, correct = 0;
    for (const a of this.state.attempts) a.answers.forEach((answer, i) => {
      if (!answer || answer.choice === null) return;
      if (date) { const d = new Date(answer.at); const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`; if (key !== date) return; }
      solved++; if (answer.choice === a.questions[i].answer) correct++;
    });
    return { solved, correct, rate: solved ? Math.round(100 * correct / solved) : null };
  }
  progress() {
    const complete = leaves.filter(t => this.state.topics[t.id]?.completed).length;
    return { complete, total: leaves.length, remaining: leaves.length - complete, percent: Math.round(100 * complete / leaves.length) };
  }
}
