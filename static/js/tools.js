$(document).ready(function(){
	$("#toolBackTo").hide();
	$(function (){
		$(window).scroll(function () {	
			if ($(this).scrollTop() > 100) {	
				$('#toolBackTo').fadeIn();	
			} else {	
				$('#toolBackTo').fadeOut();	
			}	
		});
		$('.back-top').click(function () {	
			$('body,html').animate({	
				scrollTop: 0	
			}, 500);	
			return false;	
		});	
	});
	//get width
	$(window).resize(function() {
		var width = $(this).width();
		if (width < 1000){
			$("#bd-navi").css({"display":"none"})
			$("#hd").css({"width":"900px"})
			$("#bodier").css({"width":"900px"})
			$("#ft").css({"width":"900px"})
		}else{
			$("#bd-navi").css({"display":"block"})
			$("#hd").css({"width":"1000px"})
			$("#bodier").css({"width":"1000px"})
			$("#ft").css({"width":"1000px"})
		}
	});
	op = null;
	showNavi = function(id){
        if ((op==null)|(op=='search')){
            $("#show-search").removeClass("on");
        }else if(op=='notice'){
            $("#show-notice").removeClass("on");
        }else if(op=='account'){
            $("#show-account").removeClass("on");
        }
        if (id=='search'){
            $("#show-search").addClass("on");
            $("#bd-top").html('<div id="search" class="popup"><input type="text"></input><button type="submit">搜</button></div>');
            op = 'search';
        }else if(id=='notice'){
            $("#show-notice").addClass("on");
            $("#bd-top").html('<div id="notice" class="popup"><span><a>邀&nbsp;请(2)</a></span><span><a>活&nbsp;动(3)</a></span></div>');
            op = 'notice';
        }else if(id=='account'){
            $("#show-account").addClass("on");
            $("#bd-top").html('<div id="account" class="popup"><ul><li><a>设&nbsp;&nbsp;&nbsp;置</a></li><li><a>退&nbsp;&nbsp;&nbsp;出</a></li></ul></div>');
            op = 'account';
        }
};

//	showNavi(id);
	editBox();
//	$.jGrowl("嘻哈户外,与您同在.", { life: 10000 });
});

editBox = function(){
    $(".submit").click(function(){
         $(this).parent().hide();
    })
    $(".cancel").click(function(){
        $(this).parent().hide();
    })
};


selectPackage = function(id){
	$.ajax({
		type : "POST",
		url: "ajaxcommon.php?act=getProduct&id=" + id,
		dataType : "json",
		success : function(backInfo) {
			if(backInfo.error == 0){
				$("#dialog").html(backInfo.popinfo);
				$("#dialog").dialog({
					title:"",
					height:500,
					width:500,
					modal:true,
					resizable:false
				});	
				$(".ui-dialog-titlebar").hide();
				$(".ui-widget-content").css("border","none");	
			}else{
				$("#email_tip").eq(backInfo.postion).html(backInfo.msg);
			}
		}
	});
};

attetion = function(id){
    alert("attetion");
}