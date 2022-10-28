<%!
  import urllib
%>


<%inherit file="basepage.mako"/>


<%block name="html_head">
  ${parent.html_head()}
  <link rel="stylesheet" type="text/css" href="/static/perspective_template.css">
  <style type="text/css">
    body {
      background-image: var(--背景图案-${next.context['article_subcategory']});
    }
  </style>
</%block>

  
  <section id="perspective-articles-list">
    <ul>
    <h2>远卓观点 • <span><a href="/our_perspectives/#articles-anchor">${next.context['article_subcategory']}</a></span></h2>
    % for atcl in articles_list_under_this_subcategory:
      % if atcl[0] == next.context['article_identifier']:
      <li title="${atcl[1]['article_title']}" class="currently_selected_article"><a href="/our_perspectives/perspective_article?article_identifier=${atcl[0]}">${atcl[1]['article_title']}</a></li>
      % else:
      <li title="${atcl[1]['article_title']}"><a href="/our_perspectives/perspective_article?article_identifier=${atcl[0]}">${atcl[1]['article_title']}</a></li>
      % endif
    % endfor
    </ul>
  </section>

  <h1 class="article-title">${next.context['article_title']}</h1>
  <p id="editor-logo">远卓团队编辑</p>
  
  <section class="main-section">
  
    <article>${next.body()}</article>
  </section>
  
  <section id="copyright-disclaimer">
    <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">
      <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/3.0/88x31.png" />
    </a>
    <div>This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.</div>
  </section>