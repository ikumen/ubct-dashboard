import { writable } from 'svelte/store';

export const UserApps = (function(){
  const { subscribe, set, update} = writable([]);
  return {
    subscribe,
    push: (app) => update(lst => [...lst, app]),
    pushAll: (apps) => update(lst => [...lst, ...apps]),
    remove: (app) => update(lst => [...lst.filter(li => li.id !== app.id)]),
    reset: () => set([])
  };
})();