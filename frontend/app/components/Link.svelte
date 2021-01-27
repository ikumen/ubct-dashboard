<script>
  export let url;
  export let disabled = false;
</script>

{#if disabled}
  <span class="gray">
    <slot></slot>
  </span>
{:else}
  <a class="link" href={url}>
    <slot></slot>
  </a>
{/if}
