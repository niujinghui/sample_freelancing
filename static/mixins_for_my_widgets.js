console.log("start loading mixins_for_my_widgets.js!");


export const mixin_appendCssStyle = {
    _append_cssStyle({ css_code, style_tag_id }) {
        const s = document.createElement('style');
        s.type = 'text/css';
        s.id = style_tag_id;
        s.appendChild(document.createTextNode(css_code));
        const num_of_style_element_already_exist = this.shadowRoot.querySelectorAll("style").length;
        this.shadowRoot.querySelectorAll("style")[num_of_style_element_already_exist - 1]
            .insertAdjacentElement("afterend", s);
    }
};


console.log("end loading mixins_for_my_widgets.js!");