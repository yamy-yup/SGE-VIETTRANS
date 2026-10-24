(function(){
  var $=function(s,c){return (c||document).querySelector(s)};
  var $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};

  /* Menu trên điện thoại */
  var mb=$('#menu-btn'),nav=$('#nav');
  function closeAll(){
    nav.classList.remove('open');
    mb.setAttribute('aria-expanded','false');mb.setAttribute('aria-label','Mở menu');
    $$('.dd',nav).forEach(function(d){d.classList.remove('open');$('.dd-btn',d).setAttribute('aria-expanded','false')});
  }
  mb.addEventListener('click',function(){
    var o=nav.classList.toggle('open');
    mb.setAttribute('aria-expanded',o?'true':'false');
    mb.setAttribute('aria-label',o?'Đóng menu':'Mở menu');
  });

  /* Menu xổ xuống: bấm mũi tên để mở, bấm ra ngoài hoặc Esc để đóng */
  $$('.dd',nav).forEach(function(d){
    var btn=$('.dd-btn',d);
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      var o=!d.classList.contains('open');
      $$('.dd',nav).forEach(function(x){x.classList.remove('open');$('.dd-btn',x).setAttribute('aria-expanded','false')});
      d.classList.toggle('open',o);
      btn.setAttribute('aria-expanded',o?'true':'false');
    });
  });
  document.addEventListener('click',function(e){
    if(!nav.contains(e.target)&&!mb.contains(e.target))closeAll();
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){closeAll();if(document.activeElement&&nav.contains(document.activeElement))document.activeElement.blur()}
  });
  $$('a',nav).forEach(function(a){a.addEventListener('click',function(){closeAll();a.blur()})});

  var yr=$('#year');if(yr)yr.textContent=new Date().getFullYear();

  /* Bảng giá: mở đúng mục khi bấm từ menu hoặc vào bằng đường dẫn có #bang-gia-... */
  function openPrice(){
    var h=location.hash.slice(1);
    if(!h)return;
    var el=document.getElementById(h);
    if(el&&el.tagName==='DETAILS'){el.open=true;el.scrollIntoView({block:'start'})}
    else if(h==='bang-gia'){var f=$('.pg');if(f&&!$('.pg[open]'))f.open=true}
  }
  window.addEventListener('hashchange',openPrice);
  openPrice();
})();
