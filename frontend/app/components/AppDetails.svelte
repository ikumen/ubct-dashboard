<script>
  export let app;
  export let onDelete;
</script>

<div class="fl w-100 mv1 bg-washed-yellow pa2">
  <div class="fl w-100 flex">
    <div class="fl flex-auto f5 f4-ns">{app.name}</div>
    <div class="tr w-20 w-10-l">
      <button class="f7 button-reset pv1 ph2 br1 tc bn bg-red hover-bg-light-red white pointer"
        on:click={() => onDelete(app)}
        >Delete</button>
    </div>
  </div>
  <div class="fl w-100 f5 f4-ns fw2">{app.description}</div>
  <div class="fl w-100 f6 f5-ns fw2 i pt2">{app.token}</div>
</div>