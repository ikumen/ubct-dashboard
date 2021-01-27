<script>
  import { User } from '../stores/User';

  export let secured = false;
  export let showSignin = false;
</script>

<style>
  .layout {
    height: 100%;
    min-height: 100%;
    display: flex;
    flex-direction: column;
  }

  .layout > main {
    padding-bottom: 40px;
    flex: 1 0 auto;
  }
  
  .layout > footer {
    flex-shrink: 0;
  }
</style>

<div class="layout">
  <main class="fl cf w-100 ph1 ph3-m ph6-l fw2">
  {#if secured}
    {#await $User then user}
      {#if user.isVerified}
        <slot name="verified"></slot>
      {:else if user.authenticated}
        <slot name="unverified"></slot>
      {/if}      
    {/await}
  {:else}
    <slot></slot>
  {/if}
</main>

  <footer class="footer">
    <div class="fl w-100 pt3 pb3 ph1 ph3-m ph6-l flex items-center gray bt b--light-gray">
      <div class="w-20 fl f6 o-60 nowrap">&copy; <a href="//github.com/ikumen" class="link">ikumen</a></div>
      <div class="w-80 tr f6">
        <a class="ml3 link" href="//github.com/ikumen/ubtsct-data-api">about</a>
        <a class="ml3 link gray" href="/help">help</a>
        {#if (showSignin || secured)}
          {#await $User then user}
            {#if user.authenticated}
              <a class="link ml3 gray" href="/signout">signout</a>
            {:else}
              <a class="link ml3" href="/">signin</a>
            {/if}
          {/await}
        {/if}      
      </div>
    </div>
  </footer>
</div>