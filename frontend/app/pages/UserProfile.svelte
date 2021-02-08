<script>
  import Layout from '../components/Layout.svelte';
  import AppDetails from '../components/AppDetails.svelte';
  import { UserApps } from '../stores/UserApps';
  import ErrorMessages from '../components/ErrorMessages.svelte';
  import PageTitle from '../components/PageTitle.svelte';
  import SiteHeader from '../components/SiteHeader.svelte';
  import { User } from '../stores/User';
  import { Errors } from '../stores/Errors';
  
  const emptyApp = () => ({name: '', description: ''});

  let newApp = emptyApp();

  function clearInputs() {
    newApp = emptyApp();
  }

  async function registerApp() {
    fetch('/api/user/apps', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(newApp)
      }).then(resp => {
        if (resp.status !== 201) {
          Errors.push("Oh noes, we were unable to register your app, please try again later.")
        } else {
          return resp;
        }
      })
      .then(resp => resp.json())
      .then(UserApps.push)
      .then(clearInputs);
  }

  async function fetchApps() {
    return fetch('/api/user/apps')
      .then(resp => resp.json())
      .then(UserApps.pushAll);
  } 

  async function deleteApp(app) {
    fetch(`/api/user/apps/${app.id}`, {method: 'delete'})
      .then(resp => {
        if (resp.status !== 200) {
          Errors.push(`Oh noes, we were unable to delete app: ${app.name}`)
        }
      })
      .then(() => UserApps.remove(app));
  }

  async function deleteAccount(user) {
    if (prompt(`Please enter "${user.name}" to confirm you want to delete your account.`) === user.name) {
      fetch('/api/user', {method: 'delete'})
        .then(resp => {
          if (resp.status !== 200) {
            Errors.push('Oh noes, we were unable to complete your request, please try again later.')
          } else {
            return resp;
          }
        })
        .then(() => window.location.href = '/signout');
    }
  }

</script>

<Layout secured={true}>
<div class="fl cf w-100 f4" slot="verified">
  <SiteHeader/>
  <ErrorMessages />
  <h2 class="gray mv2 f3 fw4">
    {#await $User then user}
      {user.name}
    {/await}
  </h2>
  <PageTitle title="Your apps" />
  
  <form class="fl flex-ns w-100 dib" on:submit|preventDefault={registerApp}>
    <div class="fl cf w-40 w-30-ns">
      <input type="text" class="w-100 f5 input-reset bn fl black-80 bg-white pa2 lh-solid" 
      bind:value={newApp.name}
      placeholder="name">
    </div>
    <div class="fl cf w-60 flex-auto-ns pl2">
      <input type="text" class="w-100 f5 input-reset bn black-80 bg-white pa2 lh-solid" 
        bind:value={newApp.description}
        placeholder="description">
    </div>
    <div class="fl cf w-100 w-10-ns mt2 mt0-ns pl2-ns">
      <button class="f4 w-100 pt1 pb2 br1 button-reset bn bg-blue hover-bg-light-blue white pointer b">&plus;</button>
    </div>
  </form>
  <ul class="fl w-100 list pa0">
    {#await fetchApps()}
      <li>...loading user apps</li>
    {:then} 
      {#each $UserApps as app}
      <li class="fl w-100 flex">
        <AppDetails app={app} onDelete={deleteApp} />
      </li>      
      {/each}
    {/await}
  </ul>
  {#await $User then user}
  <div class="fl cf w-100 mt4 bt b--black-10">
    <h2 class="fl cf w-100 pv0 mt2 f4 mb3">Danger zone</h2>
    <div class="fl cf w-100 mt2 mt0-ns">
      <button class="f7 ph3 pv2 br1 button-reset bn bg-red hover-bg-light-red white pointer"
        on:click={() => deleteAccount(user)}>Delete Account</button>
    </div>   
  </div>  
  {/await}
</div>
</Layout>