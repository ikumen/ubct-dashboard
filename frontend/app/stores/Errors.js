import { writable } from 'svelte/store';

export const Errors = (function(){
  const { subscribe, set, update} = writable([]);
  return {
    subscribe,
    push: (m) => update(msgs => [...msgs, m]),
    remove: (m) => update(msgs => [...msgs.filter(msg => msg !== m)]),
    reset: () => set([])
  };
})();