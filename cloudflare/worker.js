// FANTASY — Huyền Thoại Lục Địa: Worker phục vụ game dạng TÁCH FILE từ KV.
// Từ 2026-11-28 (tối ưu dung lượng theo trần ~1GB anh Do cho): trang chủ là
// index_split (bản tách), ảnh game nằm ở các key data_1..data_N (mỗi key là
// một file assets-data-N.js ~3.4MB, dưới trần 25MB/key của KV; tổng dung
// lượng nhiều key cộng lại có thể lên tới ~1GB). Bản một-file cũ vẫn giữ ở
// key index_html, xem tại /mono (dự phòng/đối chứng).
// Lưu ý: helper cf.py gắn binding với tên cố định "QUIZ_KV" — ở đây binding
// đó trỏ tới namespace FANTASY_GAME của game (không phải QUIZ_KV của Tokutei).
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return new Response("ok", { headers: { "Content-Type": "text/plain" } });
    }
    const dataMatch = url.pathname.match(/^\/assets-data-(\d+)\.js$/);
    if (dataMatch) {
      const js = await env.QUIZ_KV.get("data_" + dataMatch[1]);
      if (!js) {
        return new Response("Not found", { status: 404 });
      }
      return new Response(js, {
        headers: {
          "Content-Type": "application/javascript; charset=utf-8",
          "Cache-Control": "public, max-age=3600",
          "X-Content-Type-Options": "nosniff",
        },
      });
    }
    if (url.pathname === "/mono") {
      // Ban mono da vuot gioi han KV tu v0.7.0 (29MB) — chuyen huong ve ban split.
      return Response.redirect(new URL("/", url).toString(), 302);
    }
    if (url.pathname === "/" || url.pathname === "/index.html") {
      const html = await env.QUIZ_KV.get("index_split");
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
