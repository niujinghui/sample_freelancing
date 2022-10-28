console.log("admin.js just invoked!");


tinymce.init({
  selector: "#article_body",
  plugins: 'a11ychecker advcode casechange image formatpainter linkchecker autolink lists checklist media mediaembed pageembed permanentpen powerpaste table advtable tinycomments tinymcespellchecker',
  toolbar: 'a11ycheck addcomment showcomments casechange checklist formatpainter pageembed permanentpen table image',
  file_picker_types: 'image',
  images_upload_handler: function(blobInfo, success, failure, progress) {
    var xhr, formData;

    xhr = new XMLHttpRequest();
    xhr.withCredentials = false;
    xhr.open('POST', 'uploading_image');

    xhr.upload.onprogress = function(e) {
      progress(e.loaded / e.total * 100);
    };

    xhr.onload = function() {
      var json;

      if (xhr.status === 403) {
        failure('HTTP Error: ' + xhr.status, { remove: true });
        return;
      }

      if (xhr.status < 200 || xhr.status >= 300) {
        failure('HTTP Error: ' + xhr.status);
        return;
      }

      json = JSON.parse(xhr.responseText);

      if (!json || typeof json.location != 'string') {
        failure('Invalid JSON: ' + xhr.responseText);
        return;
      }

      success(json.location);
    };

    xhr.onerror = function() {
      failure('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
    };

    formData = new FormData();
    formData.append('file', blobInfo.blob(), blobInfo.filename());

    xhr.send(formData);
  },
  toolbar_mode: 'floating',
  tinycomments_mode: 'embedded'
});


document.addEventListener('DOMContentLoaded', evt => {
  evt.preventDefault();

  const build_node_helper = ($attaching_to_ul, node) => {
    const node_name = node[0],
      node_payload = node[1];
    const $node_li = document.createElement('LI');
    $node_li.textContent = node_name;
    if (Array.isArray(node_payload)) {
      if (node_payload.length > 0) {
        const $node_sub_ul = document.createElement('UL');
        $node_li.appendChild($node_sub_ul);
        node_payload.forEach(subnode => {
          build_node_helper($node_sub_ul, subnode);
        });
      }
    }
    else { // found an article node:
      $node_li.textContent = node_payload.article_title;
      $node_li.classList.add("exisiting-article");
      $node_li.dataset.article_identifer = node_name;
      const action_btn = document.createElement("I");
      action_btn.classList.add("far", "fa-trash-alt");
      action_btn.setAttribute("role", "delete-button");
      $node_li.appendChild(action_btn);
    }
    $attaching_to_ul.appendChild($node_li);
  };

  const update_articles_structure_map = async function() {
    // 清空：
    const container = document.getElementById("exisiting-articles-structure");
    container.innerHTML = '';

    const response = await fetch("get_existing_articles_structure", {
      "method": "POST"
    });
    if (response.status === 200) {
      const current_structure_map = await response.json();
      const special_offers_branch = current_structure_map[1][1],
        perspectives_branch = current_structure_map[1][0];
      //write the "all_special_offers" branch:
      const $root_ul_offers = document.createElement("UL");
      build_node_helper($root_ul_offers, special_offers_branch);
      //write the "our_perspectives" branch:
      const $root_ul_perspectives = document.createElement("UL");
      build_node_helper($root_ul_perspectives, perspectives_branch);
      container.appendChild($root_ul_offers);
      container.appendChild($root_ul_perspectives);
    }
  };

  update_articles_structure_map();

  const uploading_form = document.getElementById("article-uploading");
  uploading_form.addEventListener("submit", evt => {
    evt.preventDefault();

    tinymce.triggerSave();

    const data_for_backend = new FormData(uploading_form);
    const node_path = [];
    node_path.push(data_for_backend.get("article_group"));
    data_for_backend.delete("article_group");
    if (data_for_backend.get("article_category")) {
      node_path.push(data_for_backend.get("article_category"));
      data_for_backend.delete("article_category");
    }
    if (data_for_backend.get("article_subcategory")) {
      node_path.push(data_for_backend.get("article_subcategory"));
      data_for_backend.delete("article_subcategory");
    }
    data_for_backend.append("node_path", node_path);
    fetch("uploading_article", {
        "method": 'POST',
        "body": data_for_backend
      })
      .then(response => {
        if (response.status !== 200) {
          console.log('Looks like there was a problem. Status Code: ' +
            response.status);
          return;
        }
        const feedback = response.text();
        feedback.then(r => {
          alert(r);
          update_articles_structure_map();
          document.querySelector("widget-tabs").switch_tab("exisiting-articles-structure");
        });
      })
      .catch(console.log);
  });


  document.querySelector("widget-tabs").addEventListener("click", async(evt) => {
    // delete function:
    if (evt.target.matches("i.far[role='delete-button'")) {
      const deleting_entry = evt.target.closest("li.exisiting-article");
      const deleting_entry_indentifier = deleting_entry.dataset.article_identifer;
      if (confirm(`你确定要删掉已经上传的文章《${deleting_entry_indentifier}》吗？`)) {
        const form_data = new FormData();
        form_data.append("deleting_entry_indentifier", deleting_entry_indentifier);
        const response = await fetch("delete_an_article", {
          "method": "POST",
          "body": form_data
        });
        alert(await response.text());
        deleting_entry.remove();
      }
    }
  });

  // 根据不同的文章组选项，隐藏或者显示对应的输入栏：
  const hidable_inputs = [...document.querySelectorAll(".hidable_inputs")];
  const $page_selector = document.getElementById("article_group");
  $page_selector.addEventListener("change", evt => {
    if (evt.target.value === "all_special_offers") {
      hidable_inputs.forEach(elm => {
        elm.style.opacity = "0.1";
        elm.disabled = true;
      });
    }
    else {
      hidable_inputs.forEach(elm => {
        elm.style.opacity = null;
        elm.disabled = false;
      });
    }
  });
}, false);
