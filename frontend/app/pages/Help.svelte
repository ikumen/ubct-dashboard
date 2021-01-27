<script>
  import Layout from '../components/Layout.svelte';
  import PageTitle from '../components/PageTitle.svelte';
  import SiteHeader from '../components/SiteHeader.svelte';
</script>

<style>
  pre {
    white-space:pre-line;
    padding-top: 4px;
    padding-bottom: 4px;
  }

  code, pre {
    background-color: #fffceb;
    padding-left: 10px;
    padding-right: 10px;
    font-family: monospace;
    font-size: .8rem;
  }
</style>

<Layout showSignin={true}>
<div class="fl cf w-100 f4">
  <SiteHeader showNav={true} />
  <PageTitle title="Help" />

  <div class="f5">
    <section class="mb4">
      <h3 class="f5">Sign in</h3>
      Sign in is managed via third party identity providers. I try to keep the scope of each request
      to the identity providers at a bare minimum&mdash;enough to capture a unique identifier for each user. 
      Below is the list of current identity providers and what is collected/stored in our local database.

      <ul>
        <li><b>GitHub</b>: login id, and name</li>
        <li><b>Microsoft</b>: oid, and only name portion of your email</li>
      </ul>
      
      I do not store, read nor do anything with any associated access tokens granted by the providers&mdash;they
      are simply discarded. 

    </section>  
    <section>
      <h3 class="f5">API</h3>
      <h4 class="f6">Authentication</h4>
      To use the API
      <ol>
        <li><a class="link" href="/user">register an app</a> and take note of the app token (keep the token safe, don't check it into source control)</li>
        <li>send the token with every request to this server, specifically in the header section of the request payload.
          <pre class="f7 ml2 pa2 bg-washed-yellow">
            url = 'https://ubtsct-data-api./api/users'
            headers = {'{'}'auth': 'your-generated-app-token'{'}'}

            r = requests.get(url, headers=headers)
          </pre>
        </li>
        <li>every request must be via <code>https</code></li>
      </ol>
    </section>
    <section>
      <h4 class="f6">Users</h4>
      The <code>users</code> endpoint provides the following.
    </section>
  </div>
</div>  
</Layout>