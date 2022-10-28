console.log("start executing widget_tabs.js!");

import { MyHelpers } from "/static/my_helper_funcs.js";


const $template = document.createElement('template');
$template.innerHTML = `
<style>
    @import url("https://use.fontawesome.com/releases/v5.6.3/css/all.css")
</style>
<style type="text/css">
    @import url("/static/shadow_penetrating_styles.css")
</style>
<style type="text/css">
  div#widget_tabs_shadow_wrapper {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr;
  }
  div#tabs-header {
    grid-column: 1 / 2;
    grid-row: 1 / 2;
    display: flex;
    flex-wrap: wrap;
  }
  ::slotted([slot="widget_tabs-header"]) {
    width: max-content !important;
    margin: 0 !important;
    cursor:pointer;
    border: solid 1px darkgray;
    padding: 0.5em;
    border-radius: 0.3em 0.3em 0 0;
    background-color: lightgray;
    opacity: 0.3;
    transition: all 0.5s;
  }
  span#place-filler {
    flex-grow: 1;
    border-bottom: solid 1px darkgray;
    border-radius: 0.3em 0.3em 0 0;
  }
  ::slotted([slot="widget_tabs-header"].chosen) {
    border-bottom: transparent;
    background-color: initial;
    opacity: initial;
  }
  ::slotted([slot="widget_tabs-pane"]) {
    grid-column: 1 / 2;
    grid-row: 2 / 3;
    visibility: hidden;
    z-index: -1;
    border: solid 1px darkgray;
    border-top: 0;
    padding: 2em 1em;
  }
  ::slotted([slot="widget_tabs-pane"].chosen) {
    visibility: initial;
    z-index: initial;
  }
</style>

<div id="widget_tabs_shadow_wrapper">

  <div id="tabs-header">
    <slot name="widget_tabs-header"></slot>
    <span id="place-filler"></span>
  </div>

  <slot name="widget_tabs-pane"></slot>

</div>
`;

export class WidgetTabs extends HTMLElement {

  constructor() {
    console.log("WidgetTabs 里面的 constructor 开始执行！");
    // Always call super first in constructor
    super();

    // Create a shadow root
    const shadow = this.attachShadow({ mode: 'open' });
    shadow.appendChild($template.content.cloneNode(true));

    // collect all tab_headers:
    this.all_tabheaders = {};
    [...this.querySelectorAll(`[slot="widget_tabs-header"]`)].forEach(n => {
      this.all_tabheaders[n.dataset.pointing_to_pane] = n;
    });
    // collect all tab_panes:
    this.all_tabpanes = {};
    [...this.querySelectorAll(`[slot="widget_tabs-pane"]`)].forEach(n => {
      this.all_tabpanes[n.id] = n;
      // get default_pane_id:
      if (n.dataset.default_pane) {
        this.default_pane_id = n.id;
      }
    });

    shadow.getElementById('tabs-header').addEventListener("click", evt => {
      const hit_tabheader = MyHelpers.catch_event_in_bubblePath({
        event: evt,
        target_selector: "[slot='widget_tabs-header']"
      });
      if (hit_tabheader) {
        this.switch_tab(hit_tabheader.dataset.pointing_to_pane);
      }
    });
  }

  connectedCallback() {
    const default_pane_id = this.default_pane_id || Object.keys(this.all_tabpanes)[0];
    this.switch_tab(default_pane_id);
  }

  switch_tab(pane_id) {
    // 抹掉先前的选取：
    if (this.currently_chosen) {
      this.currently_chosen.tabheader.classList.remove("chosen");
      this.currently_chosen.tabpane.classList.remove("chosen");
    }
    // 设置新的选取：
    const chosen_tab = this.all_tabheaders[pane_id],
      chosen_pane = this.all_tabpanes[pane_id];
    chosen_tab.classList.add("chosen");
    chosen_pane.classList.add("chosen");
    this.currently_chosen = {
      "tabheader": chosen_tab,
      "tabpane": chosen_pane
    };
  }
}


console.log("新注册到 custom element registry: <widget-tabs> Element.");
window.customElements.define('widget-tabs', WidgetTabs);



console.log("end executing widget_tabs.js!");
