<!DOCTYPE html>
<html>

<head>
<%block name="html_head">
  <meta charset="utf-8"></meta>
  <meta name="viewport" content="user-scalable=no">
  <meta name="keywords" content="mdrt, 保险, 理财, 养老, 旅游, 教育, 投资, 定存, cpp, resp, rrsp, tfsa">
  <meta name="author" content="Jinghui Niu">
  <link rel="stylesheet" type="text/css" href="/static/menu.css">
  <link rel="stylesheet" type="text/css" href="/static/basepage.css">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
</%block>
</head>

<body>

  <section class="page-header">
    <div id="logo-container">
      <a href="/">
        <img id="company-logo" src="/gui_images/white_logo.jpg"></img>
        <span>您身边的财富规划师</span>
      </a>
    </div>
    
    <ul class="nav-menu">
      <li><a href="/">首页</a></li>
      <li><a href="/about">关于远卓</a></li>
      <li><a href="/all_special_offers">特别推荐</a></li>
      <li><a href="/our_perspectives">远卓观点</a></li>
      <li><a href="/our_team">远卓团队</a></li>
      <li><a href="/contact_us">联系我们</a></li>
      <li>
        <a id="language-select" href=""><img src="/gui_images/English-Language-Flag-1-icon.png"></img>English</a>
      </li>
      <li><a href="/administrator">管理员</a></li>
    </ul>
  </section>

  ${next.body()}
  
  <div id="contact-us">
  <h3>联系方式</h3>
    <p id="mailing-address">
      <i class="fas fa-home"></i>
      <span class="">办公地址：1500 – 1200 W73rd Avenue, Vancouver, BC V6P 6G5</span>
    </p>
    
    <p id="phone">
      <i class="fas fa-phone"></i>
      <span class="">联系电话：+1 778-892-4778</span>
    </p>
    
    <p id="email">
      <i class="far fa-envelope"></i>
      <span class="">电子邮箱：info@mdrtfinancial.com</span>
    </p>
    
    <p id="fax">
      <i class="fas fa-fax"></i>
      <span class="">传真：+1 604-261-2193</span>
    </p>
    
    <p id="hours">
      <i class="fas fa-clock"></i>
      <span class="">营业时间：Mon - Fri: 9am - 5pm</span>
    </p>
    
    <div class="slogan">远卓金融，您身边的财富规划师</div>
  </div>
  
</body>

</html>
