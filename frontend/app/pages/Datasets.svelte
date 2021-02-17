<script>
  import Layout from '../components/Layout.svelte';
  import ErrorMessages from '../components/ErrorMessages.svelte';
  import PageTitle from '../components/PageTitle.svelte';
  import SiteHeader from '../components/SiteHeader.svelte';

  async function fetchDatasets() {
    return fetch('/api/datasets')
      .then(resp => resp.json());
  }
</script>

<Layout secured={true}>
  <div class="fl cf w-100 f4" slot="verified">
    <SiteHeader showNav={true}/>
    <ErrorMessages />
    <PageTitle title="Dataset" />
    
    <div class="fl cf w-100 f5">
      The dataset includes all data from the <a class="link" href="https://github.com/ikumen/ubtsct-data-api#api-endpoints">API endpoints</a> (currently, Slack users, channels and messages).
      Data files are in JSON format, exported from a Mongo database. The Mongo Object ids (e.g, _id) can be ignored, and all
      regular "id" should be the primary identifier.

      <div class="fl cf w-100 mt3">
      {#await fetchDatasets()}
        <div class="fl cf w-100">...loading datasets</div>
      {:then resp}
        <div class="fl cf w-100">
          <h4>Slack data <span class="fw4">(since early Jan 2021)</span></h4>
        </div>
        <div class="fl cf w-100 flex">
          <div class="w-20">
            {resp.stats.counts.users} <br/>
            Users
          </div>
          <div class="w-20">
            {resp.stats.counts.messages} <br/>
            Messages
          </div>
          <div class="w-20">
            {resp.stats.counts.emojis} <br/>
            Emojis
          </div>
          <div class="w-20">
            {resp.stats.counts.files} <br/>
            File (urls)
          </div>
          <div class="w-20">
            {resp.stats.counts.reactions} <br/>
            Reactions
          </div>
        </div>
        <div class="fl cf w-100">
          <ul class="list pa0">
          {#each resp.datasets as dataset}
            <li><a class="link" href="/dataset?f={dataset.name}" target="_">{dataset.name}</a> (~{dataset.size}MB)</li>
          {/each}
          </ul>
        </div>
      {:catch}
        <div class="fl cf w-100 red">The datasets are currentnly unavailable, please try again later</div>
      {/await}
      </div>
    </div>
  </div>
  </Layout>