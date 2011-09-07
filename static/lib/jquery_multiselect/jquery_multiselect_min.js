/*
 * jQuery MultiSelect UI Widget 1.11
 * Copyright (c) 2011 Eric Hynds
 *
 * http://www.erichynds.com/jquery/jquery-ui-multiselect-widget/
 *
 * Depends:
 *   - jQuery 1.4.2+
 *   - jQuery UI 1.8 widget factory
 *
 * Optional:
 *   - jQuery UI effects
 *   - jQuery UI position utility
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 */
(function(d){var i=0;d.widget("ech.multiselect",{options:{header:!0,height:175,minWidth:225,classes:"",checkAllText:"Check all",uncheckAllText:"Uncheck all",noneSelectedText:"Select options",selectedText:"# selected",selectedList:0,show:"",hide:"",autoOpen:!1,multiple:!0,position:{}},_create:function(){var a=this.element.hide(),b=this.options;this.speed=d.fx.speeds._default;this._isOpen=!1;a=(this.button=d('<button type="button"><span class="ui-icon ui-icon-triangle-2-n-s"></span></button>')).addClass("ui-multiselect ui-widget ui-state-default ui-corner-all").addClass(b.classes).attr({title:a.attr("title"), "aria-haspopup":!0,tabIndex:a.attr("tabIndex")}).insertAfter(a);(this.buttonlabel=d("<span />")).html(b.noneSelectedText).appendTo(a);var a=(this.menu=d("<div />")).addClass("ui-multiselect-menu ui-widget ui-widget-content ui-corner-all").addClass(b.classes).insertAfter(a),c=(this.header=d("<div />")).addClass("ui-widget-header ui-corner-all ui-multiselect-header ui-helper-clearfix").appendTo(a);(this.headerLinkContainer=d("<ul />")).addClass("ui-helper-reset").html(function(){return b.header===!0?  '<li><a class="ui-multiselect-all" href="javascript:void(0)"><span class="ui-icon ui-icon-check"></span><span>'+b.checkAllText+'</span></a></li><li><a class="ui-multiselect-none" href="javascript:void(0)"><span class="ui-icon ui-icon-closethick"></span><span>'+b.uncheckAllText+"</span></a></li>":typeof b.header==="string"?"<li>"+b.header+"</li>":""}).append('<li class="ui-multiselect-close"><a href="javascript:void(0)" class="ui-multiselect-close"><span class="ui-icon ui-icon-circle-close"></span></a></li>').appendTo(c);(this.checkboxContainer=d("<ul />")).addClass("ui-multiselect-checkboxes ui-helper-reset").appendTo(a); this._bindEvents();this.refresh(!0);b.multiple||a.addClass("ui-multiselect-single")},_init:function(){this.options.header===!1&&this.header.hide();this.options.multiple||this.headerLinkContainer.find(".ui-multiselect-all, .ui-multiselect-none").hide();this.options.autoOpen&&this.open();this.element.is(":disabled")&&this.disable()},refresh:function(a){var b=this.options,c=this.menu,e=this.checkboxContainer,h=[],f=[],g=this.element.attr("id")||i++;this.element.find("option").each(function(a){d(this); var e=this.parentNode,c=this.innerHTML,i=this.title,m=this.value,a=this.id||"ui-multiselect-"+g+"-option-"+a,j=this.disabled,l=this.selected,k=["ui-corner-all"];e.tagName.toLowerCase()==="optgroup"&&(e=e.getAttribute("label"),d.inArray(e,h)===-1&&(f.push('<li class="ui-multiselect-optgroup-label"><a href="javascript:void(0)">'+e+"</a></li>"),h.push(e)));j&&k.push("ui-state-disabled");l&&!b.multiple&&k.push("ui-state-active");f.push('<li class="'+(j?"ui-multiselect-disabled":"")+'">');f.push('<label for="'+a+'" title="'+ i+'" class="'+k.join(" ")+'">');f.push('<input id="'+a+'" name="multiselect_'+g+'" type="'+(b.multiple?"checkbox":"radio")+'" value="'+m+'" title="'+c+'"');l&&(f.push(' checked="checked"'),f.push(' aria-selected="true"'));j&&(f.push(' disabled="disabled"'),f.push(' aria-disabled="true"'));f.push(" /><span>"+c+"</span></label></li>")});e.html(f.join(""));this.labels=c.find("label");this._setButtonWidth();this._setMenuWidth();this.button[0].defaultValue=this.update();a||this._trigger("refresh")},update:function(){var a= this.options,b=this.labels.find("input"),c=b.filter(":checked"),e=c.length,a=e===0?a.noneSelectedText:d.isFunction(a.selectedText)?a.selectedText.call(this,e,b.length,c.get()):/\d/.test(a.selectedList)&&a.selectedList>0&&e<=a.selectedList?c.map(function(){return this.title}).get().join(", "):a.selectedText.replace("#",e).replace("#",b.length);this.buttonlabel.html(a);return a},_bindEvents:function(){function a(){b[b._isOpen?"close":"open"]();return!1}var b=this,c=this.button;c.find("span").bind("click.multiselect", a);c.bind({click:a,keypress:function(a){switch(a.which){case 27:case 38:case 37:b.close();break;case 39:case 40:b.open()}},mouseenter:function(){c.hasClass("ui-state-disabled")||d(this).addClass("ui-state-hover")},mouseleave:function(){d(this).removeClass("ui-state-hover")},focus:function(){c.hasClass("ui-state-disabled")||d(this).addClass("ui-state-focus")},blur:function(){d(this).removeClass("ui-state-focus")}});this.header.delegate("a","click.multiselect",function(a){if(d(this).hasClass("ui-multiselect-close"))b.close(); else b[d(this).hasClass("ui-multiselect-all")?"checkAll":"uncheckAll"]();a.preventDefault()});this.menu.delegate("li.ui-multiselect-optgroup-label a","click.multiselect",function(a){a.preventDefault();var c=d(this),f=c.parent().nextUntil("li.ui-multiselect-optgroup-label").find("input:visible:not(:disabled)"),g=f.get(),c=c.parent().text();b._trigger("beforeoptgrouptoggle",a,{inputs:g,label:c})!==!1&&(b._toggleChecked(f.filter(":checked").length!==f.length,f),b._trigger("optgrouptoggle",a,{inputs:g, label:c,checked:g[0].checked}))}).delegate("label","mouseenter.multiselect",function(){d(this).hasClass("ui-state-disabled")||(b.labels.removeClass("ui-state-hover"),d(this).addClass("ui-state-hover").find("input").focus())}).delegate("label","keydown.multiselect",function(a){a.preventDefault();switch(a.which){case 9:case 27:b.close();break;case 38:case 40:case 37:case 39:b._traverse(a.which,this);break;case 13:d(this).find("input")[0].click()}}).delegate('input[type="checkbox"], input[type="radio"]', "click.multiselect",function(a){var c=d(this),f=this.value,g=this.checked,i=b.element.find("option");this.disabled||b._trigger("click",a,{value:f,text:this.title,checked:g})===!1?a.preventDefault():(c.attr("aria-selected",g),i.each(function(){if(this.value===f)(this.selected=g)?this.setAttribute("selected","selected"):this.removeAttribute("selected");else if(!b.options.multiple)this.selected=!1}),b.options.multiple||(b.labels.removeClass("ui-state-active"),c.closest("label").toggleClass("ui-state-active", g),b.close()),b.element.trigger("change"),setTimeout(d.proxy(b.update,b),10))});d(document).bind("mousedown.multiselect",function(a){b._isOpen&&!d.contains(b.menu[0],a.target)&&!d.contains(b.button[0],a.target)&&a.target!==b.button[0]&&b.close()});d(this.element[0].form).bind("reset.multiselect",function(){setTimeout(function(){b.update()},10)})},_setButtonWidth:function(){var a=this.element.outerWidth(),b=this.options;if(/\d/.test(b.minWidth)&&a<b.minWidth)a=b.minWidth;this.button.width(a)},_setMenuWidth:function(){var a= this.menu,b=this.button.outerWidth()-parseInt(a.css("padding-left"),10)-parseInt(a.css("padding-right"),10)-parseInt(a.css("border-right-width"),10)-parseInt(a.css("border-left-width"),10);a.width(b||this.button.outerWidth())},_traverse:function(a,b){var c=d(b),e=a===38||a===37,c=c.parent()[e?"prevAll":"nextAll"]("li:not(.ui-multiselect-disabled, .ui-multiselect-optgroup-label)")[e?"last":"first"]();c.length?c.find("label").trigger("mouseover"):(c=this.menu.find("ul:last"),this.menu.find("label")[e?  "last":"first"]().trigger("mouseover"),c.scrollTop(e?c.height():0))},_toggleCheckbox:function(a,b){return function(){!this.disabled&&(this[a]=b);b?this.setAttribute("aria-selected",!0):this.removeAttribute("aria-selected")}},_toggleChecked:function(a,b){var c=b&&b.length?b:this.labels.find("input"),e=this;c.each(this._toggleCheckbox("checked",a));this.update();var h=c.map(function(){return this.value}).get();this.element.find("option").each(function(){!this.disabled&&d.inArray(this.value,h)>-1&&e._toggleCheckbox("selected", a).call(this)});c.length&&this.element.trigger("change")},_toggleDisabled:function(a){this.button.attr({disabled:a,"aria-disabled":a})[a?"addClass":"removeClass"]("ui-state-disabled");this.menu.find("input").attr({disabled:a,"aria-disabled":a}).parent()[a?"addClass":"removeClass"]("ui-state-disabled");this.element.attr({disabled:a,"aria-disabled":a})},open:function(){var a=this.button,b=this.menu,c=this.speed,e=this.options;if(!(this._trigger("beforeopen")===!1||a.hasClass("ui-state-disabled")||this._isOpen)){var h= b.find("ul:last"),f=e.show,g=a.position();d.isArray(e.show)&&(f=e.show[0],c=e.show[1]||this.speed);h.scrollTop(0).height(e.height);d.ui.position&&!d.isEmptyObject(e.position)?(e.position.of=e.position.of||a,b.show().position(e.position).hide().show(f,c)):b.css({top:g.top+a.outerHeight(),left:g.left}).show(f,c);this.labels.eq(0).trigger("mouseover").trigger("mouseenter").find("input").trigger("focus");a.addClass("ui-state-active");this._isOpen=!0;this._trigger("open")}},close:function(){if(this._trigger("beforeclose")!== !1){var a=this.options,b=a.hide,c=this.speed;d.isArray(a.hide)&&(b=a.hide[0],c=a.hide[1]||this.speed);this.menu.hide(b,c);this.button.removeClass("ui-state-active").trigger("blur").trigger("mouseleave");this._isOpen=!1;this._trigger("close")}},enable:function(){this._toggleDisabled(!1)},disable:function(){this._toggleDisabled(!0)},checkAll:function(){this._toggleChecked(!0);this._trigger("checkAll")},uncheckAll:function(){this._toggleChecked(!1);this._trigger("uncheckAll")},getChecked:function(){return this.menu.find("input").filter(":checked")}, destroy:function(){d.Widget.prototype.destroy.call(this);this.button.remove();this.menu.remove();this.element.show();return this},isOpen:function(){return this._isOpen},widget:function(){return this.menu},_setOption:function(a,b){var c=this.menu;switch(a){case "header":c.find("div.ui-multiselect-header")[b?"show":"hide"]();break;case "checkAllText":c.find("a.ui-multiselect-all span").eq(-1).text(b);break;case "uncheckAllText":c.find("a.ui-multiselect-none span").eq(-1).text(b);break;case "height":c.find("ul:last").height(parseInt(b, 10));break;case "minWidth":this.options[a]=parseInt(b,10);this._setButtonWidth();this._setMenuWidth();break;case "selectedText":case "selectedList":case "noneSelectedText":this.options[a]=b;this.update();break;case "classes":c.add(this.button).removeClass(this.options.classes).addClass(b)}d.Widget.prototype._setOption.apply(this,arguments)}})})(jQuery); 