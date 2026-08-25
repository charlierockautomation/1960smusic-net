// 1960smusic.net — Worker entry point.
// Serves the static site (via env.ASSETS) and one small API surface for the
// Daily Guessing Game leaderboard, backed by a 5-row-capped KV list.
// Everything that isn't /api/leaderboard falls straight through to assets.

const KV_KEY = 'top5';
const MAX_SCORE = 240; // 15 * 16, see docs on the Daily Guessing Game scoring table
const MAX_LEVEL = 15;
const NAME_MAX_LEN = 20;

// Deliberately small, obvious-only list. Not a substitute for moderation,
// just keeps drive-by garbage off a leaderboard nobody reviews.
const BLOCKED_SUBSTRINGS = [
  'fuck', 'shit', 'bitch', 'cunt', 'nigger', 'nigga', 'faggot', 'retard',
  'rape', 'nazi', 'hitler'
];

function isProfane(name) {
  const lower = name.toLowerCase();
  return BLOCKED_SUBSTRINGS.some((w) => lower.includes(w));
}

function expectedScore(levelReached, songsCorrectInLevel, fullClear) {
  if (fullClear) {
    return levelReached === MAX_LEVEL && songsCorrectInLevel === MAX_LEVEL ? MAX_SCORE : null;
  }
  if (levelReached < 1 || levelReached > MAX_LEVEL) return null;
  if (songsCorrectInLevel < 0 || songsCorrectInLevel >= levelReached) return null;
  return (levelReached - 1) * levelReached + songsCorrectInLevel;
}

function jsonResponse(body, status) {
  return new Response(JSON.stringify(body), {
    status: status || 200,
    headers: { 'Content-Type': 'application/json' }
  });
}

async function getLeaderboard(env) {
  const raw = await env.DAILY_LEADERBOARD.get(KV_KEY);
  if (!raw) return [];
  try {
    const list = JSON.parse(raw);
    return Array.isArray(list) ? list : [];
  } catch (e) {
    return [];
  }
}

async function handleGet(env) {
  const list = await getLeaderboard(env);
  return jsonResponse(list);
}

async function handlePost(request, env) {
  let body;
  try {
    body = await request.json();
  } catch (e) {
    return jsonResponse({ error: 'Invalid JSON.' }, 400);
  }

  const name = typeof body.name === 'string' ? body.name.trim() : '';
  const score = Number(body.score);
  const levelReached = Number(body.level_reached);
  const songsCorrectInLevel = Number(body.songs_correct_in_level);
  const fullClear = !!body.full_clear;

  if (!name || name.length > NAME_MAX_LEN) {
    return jsonResponse({ error: 'Name must be 1-' + NAME_MAX_LEN + ' characters.' }, 400);
  }
  if (isProfane(name)) {
    return jsonResponse({ error: 'Please choose a different name.' }, 400);
  }
  if (!Number.isInteger(score) || !Number.isInteger(levelReached) || !Number.isInteger(songsCorrectInLevel)) {
    return jsonResponse({ error: 'Malformed score submission.' }, 400);
  }
  const expected = expectedScore(levelReached, songsCorrectInLevel, fullClear);
  if (expected === null || expected !== score) {
    return jsonResponse({ error: 'Score is not internally consistent.' }, 400);
  }

  const list = await getLeaderboard(env);
  if (list.length >= 5 && score <= list[list.length - 1].score) {
    return jsonResponse({ error: 'Score did not make today\'s top 5.', leaderboard: list }, 200);
  }

  list.push({
    name: name,
    score: score,
    level_reached: fullClear ? MAX_LEVEL : levelReached,
    date: new Date().toISOString().slice(0, 10)
  });
  list.sort((a, b) => b.score - a.score);
  const trimmed = list.slice(0, 5);
  await env.DAILY_LEADERBOARD.put(KV_KEY, JSON.stringify(trimmed));
  return jsonResponse({ leaderboard: trimmed }, 200);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/leaderboard') {
      if (request.method === 'GET') return handleGet(env);
      if (request.method === 'POST') return handlePost(request, env);
      return jsonResponse({ error: 'Method not allowed.' }, 405);
    }
    return env.ASSETS.fetch(request);
  }
};
