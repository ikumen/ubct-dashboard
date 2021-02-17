<script>
  import { User } from '../stores/User';
  export let showNav = false;
  export let isVerifiedOnly = false;
</script>

<div class="fl cf flex mt3 mb4 w-100">
  <div class="flex-auto f4 f3-l fw4">
    <span class="dn-m dn-l dib">UB</span>
    <span class="dn dib-m">Udacity Bertelsmann</span> 
    <span class="dn dib-l">Udacity Bertelsmann Cloud Track</span> 
    Data API
  </div>
  {#if showNav}
  <div class="flex-auto f6 tr">
    <ul class="list pa0 mt1">
    {#await $User then user}
    {#if user.authenticated && (!isVerifiedOnly || user.is_verified)}
      <li class="dib">
        <a class="link" href="/data">data</a>
      </li>    
      <li class="dib ml3">
        <a class="link" href="/user">profile</a>
      </li>    
      {/if}
    {/await}
    </ul>
  </div>      
  {/if}
</div>
