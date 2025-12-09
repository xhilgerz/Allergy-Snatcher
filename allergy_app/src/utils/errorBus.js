// Simple global error event bus for showing error toasts/banners.
const errorBus = new EventTarget();

export function emitError(message) {
  
  if (!message) return;
  errorBus.dispatchEvent(new CustomEvent("error", { detail: message.toString() }));
}

export function subscribeToErrors(listener) {
  errorBus.addEventListener("error", listener);
  return () => errorBus.removeEventListener("error", listener);
}
