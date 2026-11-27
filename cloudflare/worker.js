// FANTASY — Huyền Thoại Lục Địa: Worker phục vụ file game tĩnh từ KV.
// Lưu ý: helper cf.py gắn binding với tên cố định "QUIZ_KV" — ở đây binding đó
// trỏ tới namespace FANTASY_GAME của game (không phải QUIZ_KV của app Tokutei).
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return new Response("ok", { headers: { "Content-Type": "text/plain" } });
    }
    if (url.pathname === "/" || url.pathname === "/index.html") {
      const html = await env.QUIZ_KV.get("index_html");
      if (!html) {
        return new Response("Game chua duoc nap len KV.", { status: 503 });
      }
      return new Response(html, {
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          "Cache-Control": "no-store",
          "X-Content-Type-Options": "nosniff",
        },
      });
    }
    return new Response("Not found", { status: 404 });
  },
};
