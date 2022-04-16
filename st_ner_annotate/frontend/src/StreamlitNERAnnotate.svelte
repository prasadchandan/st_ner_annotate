<script lang="ts">
  import { Streamlit } from "./streamlit";
  import type { RenderData } from "./streamlit";
  import MarkedWord from "./components/MarkedWord.svelte";
  import { onMount, afterUpdate, onDestroy } from "svelte"

  let text: string = "";
  let ents: {
    start: number;
    end: number;
    label: string;
  }[] = [];
  export let label: string;
  export let disabled: boolean;
  let selectedText: Selection | null = null;
  let mounted = false;

  const onRender = (event: Event): void => {
    const data = (event as CustomEvent<RenderData>).detail;
    if (!mounted) {
      text = data.args["text"];
      ents = data.args["ents"];
      mounted = true;
    }
  };

  onMount(() => {
    Streamlit.setComponentReady();
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
    Streamlit.setFrameHeight();
  });

  afterUpdate(() => {
    Streamlit.setFrameHeight();
  });

  onDestroy(() => {
    Streamlit.events.removeEventListener(Streamlit.RENDER_EVENT, onRender);
  });

  const returnValuesToPython = (): void => {
    console.log(ents);
    Streamlit.setComponentValue(ents);
  }

  const addEntities = (start: number, end: number, entity_idx: number, label: string): void => {
    let offset;
    if (entity_idx > 0) {
        offset = ents[entity_idx - 1].end;
    }
    else {
        offset = 0;
    }

    ents.push({
      start: start + offset,
      end: end + offset,
      label: label
    });

    ents.sort((l, r): number => {
      if (l.start < r.end) return -1;
      if (l.start > r.end) return 1;
      return 0;
    });

    ents = ents;
  }

  const handleMessage = (event): void => {
    ents.splice(event.detail.id, 1);
    ents = ents;
    returnValuesToPython();
  };

  function handleMouseup(event) {
    selectedText = window.getSelection();
    let startIdx;
    let endIdx;

    if (selectedText.anchorOffset > selectedText.focusOffset) {
      startIdx = selectedText.focusOffset;
      endIdx = selectedText.anchorOffset;
    }
    else {
      startIdx = selectedText.anchorOffset;
      endIdx = selectedText.focusOffset;
    }

    if (selectedText && selectedText.toString().length > 0) {
      console.log(`Selected text ${selectedText}`);
      addEntities(
        startIdx, 
        endIdx,
        Number(selectedText.anchorNode.parentNode.className),
        label
      );
      returnValuesToPython();
    }
  }
</script>

<svelte:window on:mouseup={handleMouseup} />

<main {disabled}>
  {#each ents as { start, end, label }, i (start)}
    {#if i == 0}<span class={i}>{text.substring(0, start)}</span>{/if}
    <MarkedWord
      words={text.substring(start, end)}
      {label}
      id={i}
      on:message={handleMessage}
    />
    {#if i != ents.length - 1}
      <span class={i+1}>{text.substring(end, ents[i + 1]["start"])}</span>
    {/if}
    {#if i == ents.length - 1}<span class={i+1}>{text.substring(end)}</span>{/if}
  {:else}
    {text}
  {/each}
</main>

<style>
  main {
    padding: 1em;
    line-height: 2;
  }
</style>
