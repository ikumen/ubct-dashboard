<script>
  import { navigate } from 'svelte-routing';
  import ErrorMessages from '../components/ErrorMessages.svelte';
  import Layout from '../components/Layout.svelte';
  import PageTitle from '../components/PageTitle.svelte';
  import SiteHeader from '../components/SiteHeader.svelte';
  import { Errors } from '../stores/Errors';
  import { User } from '../stores/User';

  let snippetUrl;

  function isValidUrl(s) {
    try {
      new URL(s);
      if (s.startsWith('https://slack-files.com/T'))
        return true;
    } catch (_) {}
    Errors.push(`Invalid Slack file url: ${s}`);
    return false;
  }

  async function verifySnippet() {
    if (isValidUrl(snippetUrl)) {
      return fetch(`/api/auth/verify?u=${encodeURI(snippetUrl)}`)
        .then(async resp => {
          if (resp.status === 200) {
            User.load(await resp.json());
            navigate('/user', {replace: true});
          } else {
            const data = await resp.json();
            if (resp.status === 401) {
              Errors.push("Oh noes, it looks like your session has timed out, please login and try again.");
            } else if (resp.status === 400) {
              Errors.push(data.error);
            }
          }
        })
        .catch(resp => {
          // remember only network failures
          console.log("failed", resp.status, resp.statusText)
        })
    }
  }

</script>

<Layout secured={true}>
<div class="fl cf w-100 f4" slot="unverified">
  <SiteHeader/>
  <ErrorMessages />
  <PageTitle title="Scholar Verification" />
  <div class="fl cf w-100">
    Hi there 
    <span class="bg-washed-yellow ph1">
      {#await $User}...{:then user}{user.name}{/await}</span>, 
    it looks like this is your first time signing in with us. Let's verify you are a scholar of 
    the <a class="link" href="https://www.udacity.com/bertelsmann-tech-scholarships">Udacity Bertelsmann Tech Scholarship</a> 
    course with a little Slack challenge. 
  </div>

  <div class="fl cf w-100">
    <form on:submit|preventDefault={verifySnippet}>
      <div class="fl w-100 mt4 mb2">
        1. Simply create a <a class="link" href="https://slack.com/help/articles/204145658-Create-a-snippet">Slack text snippet</a> with this token in the content section
      </div>
      <div class="fl w-100 mv2">
        <span class="f4 pv1 ph3 bg-washed-yellow">
        {#await $User}
          ...loading token
        {:then user} 
          {user.nonce}      
        {/await}
        </span>
      </div>
      <div class="fl w-100 mt3 mb2">
        2. Make the snippet available via external link, and paste the link here
      </div>
      <div class="fl cf mv1 w-100">
        <label class="clip" for="snippetUrl">Snippet Url</label>
        <input class="f5 input-reset bn fl black-80 bg-white pa2 lh-solid w-100" 
          placeholder="Link to your snippet" 
          type="text" name="snippetUrl"
          bind:value={snippetUrl} 
          id="snippetUrl">
      </div>
      <div class="fl cf mv1 w-100">
        <input class="f5 button-reset br1 fl pv2 tc bn bg-green hover-bg-light-green white pointer ph4 mr3" 
          type="submit" value="Verify">
      </div>
    </form>
  </div>
  <div class="fl cf w-100 mt3 f5">
    <i>If you are here by accident, no worries, <a class="link" href="/signout">just click here to signout</a> and we'll forget everything.</i>
  </div>
</div>    
</Layout>  
