<script>
  import { User } from '../stores/User';
  export let showNav = false;
</script>

<div class="fl cf flex mt3 mb4 w-100">
  <div class="flex-auto f4 f3-ns fw3">
    Udacity Bertelsmann <span class="dn dib-l">Cloud Track</span> Data API
  </div>
  {#if showNav}
  <div class="flex-auto f5 fw3 tr">
    <ul class="list pa0 mt1">
    {#await $User then user}
      {#if user.authenticated}
      <li class="dib">
        <a class="link" href="/user">profile</a>
      </li>    
      {/if}
    {/await}
    </ul>
  </div>      
  {/if}
</div>
