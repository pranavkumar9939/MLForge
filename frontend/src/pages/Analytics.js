import client from "./api";

const VISITOR_KEY = "mlforge_visitor_id";

function getVisitorId() {
  let id = localStorage.getItem(VISITOR_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(VISITOR_KEY, id);
  }
  return id;
}

// Fire-and-forget - tracking must never break the page it's tracking.
export function trackPageview(path) {
  client
    .post("/analytics/pageview", {
      path,
      visitor_id: getVisitorId(),
      referrer: document.referrer || null,
    })
    .catch(() => {
      // Silently ignore - a failed analytics call is not the user's problem.
    });
}