<script>
import Layout from "../components/Layout.svelte";

  async function fetchOauthProviders() {
    return fetch('/api/auth/providers')
      .then(resp => resp.json())
      .then(providers => {
        const arr = [];
        for (const id in providers)
          arr.push({id, label: providers[id]});
        return arr;
      })
  }
</script>

<Layout>
<div class="tc">
<header class="pt4">
  <div class="pt5-ns">
    <h3 class="f4 f3-ns fw2 mv0">Udacity Bertelsmann Tech Scholarship</h3>
    <h1 class="f1-l f2-m mv0">
      Cloud Track Data API
    </h1>
  </div>
</header>
<div class="ph6-l ph4-m mv4">
  <p class="f5 fw2 f4-ns">
    A data provider for scholars enrolled in the <a class="link" href="https://www.udacity.com/bertelsmann-tech-scholarships">Udacity Bertelsmann Tech Scholarship Cloud Track</a> challenge 
    course, consume it and build something cool.
  </p>
  <ul class="list pa0 mb0 mt5">
  {#await fetchOauthProviders()}
    <li>...loading sign in providers</li>
  {:then providers}
    {#each providers as provider}
      <li><a class="f7 f6-ns fw2 btn br1 dim ph3 pv2 mb2 dib white bg-black" href="/signin/{provider.id}">Sign in with {provider.label}</a></li>
    {/each}
  {:catch error}
    <li class="red">Unable to load Sign in providers</li>
    <li class="light-gray">{error.message}</li>
  {/await}
  </ul>
</div>
</div>
</Layout>