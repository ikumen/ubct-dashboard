import { writable } from 'svelte/store';

export const User = (function(){
  const unauthenticatedUser = {authenticated: false};

  const { subscribe, set } = writable(unauthenticatedUser);

  async function fetchUser() {
    return fetch('/api/auth/user')
      .then(resp => {
        if (resp.status === 200) {
          return resp.json();
        } else if (resp.status === 401) {
          return unauthenticatedUser;
        }
      })
      .catch(() => unauthenticatedUser);
  }

  async function load(user) {
    if (!user)
      user = await fetchUser();
    set({...user, authenticated: true, isVerified: !user.nonce});
  }

  load();

  return {
    subscribe,
    load,
    reload: async () => set(await fetchUser()),
  }
})();