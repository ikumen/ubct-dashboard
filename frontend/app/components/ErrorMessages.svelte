<script>
  import { fade } from 'svelte/transition';
  import { Errors } from '../stores/Errors';
</script>

<div class="fl cf w-100">
{#each $Errors as error}
  <div class="bg-light-red flex mb2 br1 pa2 pointer" transition:fade on:click={Errors.remove(error)}>
    <div class="fl cf w-90">{error}</div>
    <div class="fl cf w-10 fw6 tr">x</div>
  </div>      
{/each}
</div>
