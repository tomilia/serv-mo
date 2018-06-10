'use strict';
$(function() {

  var app7 = new Vue({
    el: '#app-7',
    delimiters: ['${', '}'],
    data: function(){
      return {
      selection:'default',
      extrax:[],
      foodist:[],
      locselection:[]
    }
  },
  methods:{
    init:function(){

      let self=this;

      var href = window.location.href;
      var url_vars = this.getParameter();
      for(var i in url_vars)
      {
              if(i=='district')
              {
                this.locselection=(url_vars[i].split(','));
              }
              else if (i=='sort')
              {
                this.selection=url_vars[i];
              }
      }
      href=href.split('?');
      $.ajax({
      url: "/filter/",
      method :'get',
      data: href[1]
    }).done(function(data) {
      self.foodist=JSON.parse(data.numpost);
      self.extrax=data.exattr;
    });
  }
  ,
    hasPrev:function(event){
   return this.foodist[0].number>1;

 },
 hasNext:function(event){

   return this.foodist[0].number<this.foodist[0].count;

 },
 updateQueryStringParameter:function(uri, key, value) {
   var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
   var separator = uri.indexOf('?') !== -1 ? "&" : "?";
   if (uri.match(re)) {
     return uri.replace(re, '$1' + key + "=" + value + '$2');
   }
   else {
     return uri + separator + key + "=" + value;
   }
 },
 getParameter:function() {
   var vars = [], hash;
var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

for(var i = 0; i < hashes.length; i++)
{
       hash = hashes[i].split('=');
       vars[hash[0]] = hash[1];
}

return vars;
}
 ,
 get: function (ex,a) {
   return ex.cnsx_id==a.id;
 },
 choose:function(index){
   this.selection=index;
 },
loc_handler:function(name,id){
  this.locpick(id);
  this.filter(name,this.locselection);
},
checklocpick:function(id)
{
  for(var x=0;x<this.locselection.length;x++)
  {

    if(this.locselection[x]==id)return true;
  }
  return false;
},
 locpick:function(id){

   for(var x=0;x<this.locselection.length;x++)
   {
     if(this.locselection[x]==id)
     {
      this.locselection.splice(x,1);
       return;
     }
   }
   if(this.locselection.length==3)
   {
     alert('Too much boy');
     return;
   }
   this.locselection.push(id);
 },
 navsorthandler:function(arg1,name,value){
   this.choose(arg1);
   this.filter(name,value);
 },
    filter: function (name,value){

   var href = window.location.href;
   var regex = new RegExp("[&\\?]" + name + "=");
   var temp ;
   var url ;
   let self=this;

   if(regex.test(href))
   {
     regex = new RegExp("([&\\?])" + name + "=\\d+");
     temp = href.replace(regex, "$1" + name + "=" + value);
   }
   else
   {
     if(href.indexOf("?") > -1)
     {
       temp = href + "&" + name + "=" + value;
     }
     else
       temp = href + "?" + name + "=" + value;

   }
   url= temp;
   url= this.updateQueryStringParameter(url, name, value);

   url = url.split("?");

   $.ajax({
   url: "/filter/",
   method :'get',
   data: url[1]
 }).done(function(data) {

   self.foodist=JSON.parse(data.numpost);
   self.extattr=data.extattr;
 });
 var newHash = url;
 newHash=newHash[0]+"?"+newHash[1];

 if(history.pushState) {
     history.pushState(null, null, newHash);
 } else {
     location.hash = newHash;
 }
 }
  },
  created(){
    this.init();
  }
  })
      });
