<script>
  import Layout from '../components/Layout.svelte';
  import PageTitle from '../components/PageTitle.svelte';
  import SiteHeader from '../components/SiteHeader.svelte';
</script>

<Layout showSignin={true}>
<div class="fl cf w-100 f4">
  <SiteHeader showNav={true} />
  <PageTitle title="Help" />

  <div class="fl cf w-100 f5">
    <div class="fl w-100 mv3">
      <ul class="fl w-100 list ma0 pa0">
        <li><a href="#privacy" class="link">Privacy</a></li>
        <li><a href="#slack-verification" class="link">Slack Verification</a></li>
        <li><a href="#api-endpoints" class="link">API Endpoints</a></li>
      </ul>
    </div>
  
    <section class="mb4">
      <h3 id="privacy" class="fl w-100 f5">Privacy</h3>
      <div class="fl w-100">
        Authentication is through third party identity providers, using the <a href="https://auth0.com/docs/flows/authorization-code-flow" class="link">OAuth authorization code flow</a>. 
        The <a href="https://www.oauth.com/oauth2-servers/scope/defining-scopes/" class="link">scope for each request</a> to an identity provider is kept to a bare minimum&mdash;enough to capture a unique identifier for each user. 
        Below is the list of current identity providers and what is collected/stored in our local database.
      </div>  
      <div class="fl cf w-100 mt3 fw5 bg-washed-yellow">
        <div class="fl w-30 pa2">Provider</div>
        <div class="fl w-70 pa2">Data Collected</div>
      </div>
      <div class="fl cf w-100 bt b--light-gray bg-washed-yellow">
        <div class="fl w-30 pa2">GitHub</div>
        <div class="fl w-70 pa2"><a href="https://docs.github.com/en/rest/reference/users#get-the-authenticated-user" class="link">login id, and name</a></div>
      </div>
      <div class="fl cf w-100 mb2 bg-washed-yellow">
        <div class="fl w-30 pa2">Microsoft</div>
        <div class="fl w-70 pa2"><a href="https://docs.microsoft.com/en-us/azure/active-directory/develop/id-tokens#payload-claims" class="link">oid and just the name portion of your email from the JWT payload</a></div>
      </div>
      <div class="fl w-100 i">      
        No access tokens granted by the providers are stored or used in anyway, they are simply discarded. 
      </div>
    </section> 
    <section>
      <h3 id="slack-verification" class="fl w-100 mt4 f5">Slack Verification</h3>
      <div class="fl w-100">
        Once an identity provider (see above) has authenticated a user, and if the user is new to our system, we need to verify they are
        part of the Udacity Bertelsmann Tech Scholarship Cloud Track course. We assume the user is part of the course if they have access 
        to the <a href="//bertelsmanncloudtrack.slack.com/">bertelsmanncloudtrack.slack.com</a> workspace. To prove the user has access to the
        workspace, just create a snippet with a piece of challenge token that we provide. Below are instructions on creating the snippet.
      </div>
      <div class="fl w-100 mt3">
        1. Open "Create a snippet dialog" by clicking on the lightning icon from the message input, and selecting "Create a snippet"
      </div>  
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/1-shortcut.png" alt="Create snippet shortcut">
      </div>
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/2-create-snippet.png" height="280" alt="Create snippet shortcut">
      </div>
      <div class="fl w-100 mt3">
        2. In the snippet editor, paste the challenge token (from the signin verify page). Do not share (uncheck), otherwise we'll end up spamming the
        the Slack with these challenge snippets. Click "Create Snippet" button to create your snippet.
      </div>  
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/3-edit-snippet.png" height="320" alt="Create snippet shortcut">
      </div>
      <div class="fl w-100 mt3">
        3. Next we need to grab the external link to this snippet. Go to you the snippet via the "File browser" menu. You can open the "File browser"
        two ways, if you have the short cut in your main menu
      </div>  
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/5-file-browser.png" height="280" alt="Create snippet shortcut">
      </div>
      <div class="fl w-100 mt3">
        ... or "More", "File Browser" context menu that pops up.
      </div>  
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/4-file-browser.png" height="300" alt="Create snippet shortcut">
      </div>
      <div class="fl w-100 mt3">
        4. From the "File browser" page, locate the snippet, and hover over it to get the actions menu popup. Then select 
        the "Create external link" item from the context menu. 
      </div>  
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/6-select-file.png" height="280" alt="Create snippet shortcut">
      </div>
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/7-external-link.png" height="280" alt="Create snippet shortcut">
      </div>
      <div class="fl w-100 mt3">
        5. A popup with a "Public link to this file" will appear, copy the link and paste on the signin verify page.
      </div>  
      <div class="fl w-100 pv2 pl3 pr3 pr6-ns">
        <img src="/static/images/8-done.png" height="260" alt="Create snippet shortcut">
      </div>
    </section>
    <section>
      <h3 id="api-endpoints" class="fl w-100 f5">API Endpoints</h3>
      <div class="fl w-100">
        Please check visit the project page for the most up to date API endpoints.
      </div>
      <div class="fl w-100 pv2 ph3">
        <a href="https://github.com/ikumen/ubtsct-data-api#api-endpoints" class="link">https://github.com/ikumen/ubtsct-data-api#api-endpoints</a>
      </div>
    </section>
  </div>
</div>  
</Layout>