const UserService = (function() {
  let user;

  async function fetchUser({force=false}={}) {
    if (!user || force) {
      user = await fetch('/api/user')
        .then(resp => resp.json());
    } else {
      console.log('returning cached version');
    }
    return Promise.resolve(user);      
  }

  return {
    reload: async () => fetchUser({force: true}),
    current: fetchUser
  }
})();

module.exports = {
  UserService
}