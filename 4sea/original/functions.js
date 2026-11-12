var imgCounter = 0;


function baseLoad()
{
	var Menu = "";
	var menuHeight = $("#Menu").height();


	$("#Title").css({top: menuHeight});

	// set presenter's details
	var title = $("#first");  //this would just be your selector
	var prTop = title.position().top + title.outerHeight(true);
	var prLeft = ( $(document).width() / 2) - ( $(document).width() / 4);
	$("#Presenter").css({top: prTop, left: prLeft});
	Fader();

	//create menus
	for(x = 0; x<MenuItems.length; x++)
	{
		Menu += "<div class='menuItem'><p class='pointer' onclick='MenuDrive(\""+ MenuItems[x] +"\")'><bold>" + MenuItems[x] + "</bold></p></div>\n";
	}

	//show menu
	$("#leftMenu").html(Menu);
	$(".menuItem").css({paddingTop: Math.floor(menuHeight/3) +"px"});

	//set background image
	$("#BgImg")
		.attr("src","./photos/backgrounds/_MG_2746.jpg")
		.width(mainWidth)
		.height(mainHeight)
		.appendTo($('body'));


	// set facebook letter size
	var fbSize = $("#rightMenu").height();
	$(".fa").css({fontSize: 2*(fbSize /3)});

	// set footer position
	var fTop = $(document).height() -50;
	$("#Footer").css({top: fTop});

}


function MenuDrive(Item)
{

	switch (Item)
	{
		case "Home":
			if( $("#Hidden").val() == "showed")
			{
				Fader();
				setTimeout(function(){
					$("#Presenter").html("");
				},500);
			}
			break;

		case "Music":
			$.post("./scripts/list.php",{req:"music"},function(retval){

					if( $("#Hidden").val() == "showed")
					{
						Fader();
					}
					setTimeout(function(){	$("#Presenter").html(""); },200);
					setTimeout(function(){	$("#Presenter").html(retval); },200);
					Fader();

				});
			break;

		default:
            link = Item.split(" ");
			if( $("#Hidden").val() == "showed")
			{
				Fader();

			}
			setTimeout(function(){
					$("#Presenter").html("");
				},200);

			setTimeout(function(){
				$.get( link[0]+".txt", function(Text){
					$("#Presenter").html(Text);
					});
			},200);
			Fader();
			break;
	}
}

function Fader()
{

	if ( $("#Hidden").val() == "hided")
    {
		var title = $("#Title");  //this would just be your selector
		var prTop = title.position().top + $("#first").height();
        $("#Presenter").animate({
            //bottom: 'toggle',
			top: prTop,
            height: 'toggle'

        }).delay(200);
        $("#Hidden").val("showed");

    }
    else
    {
      	$("#Presenter").animate({
           	top: 0,
			height: 'toggle'

       	}).delay(500);
        $("#Hidden").val("hided");
		$("#Presenter").css({top: "0"});
    }
}


function player(ID)
{
	$("#Player").html("");
	$("#description").html("");
	$.get( ID+".txt", function(Text){
			$("#description").html(Text);
			});

	var audioPlayer = "<audio controls autoplay><source src='./music/"+ID+".mp3' type='audio/mpeg'></audio>";
	$("#Player").html(audioPlayer);

}

function signUp()
{
    var fName = document.getElementById("signupFormfname").value
    var lName = document.getElementById("signupFormlname").value
    var uName = document.getElementById("signupFormuname").value
    var eMail = document.getElementById("signupFormemail").value
    //alert (fName)

    $.post("../scripts/registration.php",{fname:fName, lname: lName, uname: uName, email: eMail, lang:"en"}, function(retval){

        if (retval == "OK")
        {
            document.getElementById("signupFormfname").value = ""
            document.getElementById("signupFormlname").value = ""
            document.getElementById("signupFormuname").value = ""
            document.getElementById("signupFormemail").value = ""
            $("#Popup-content").html("<b>Thank you for your registration!<b>");
            $("#signupButton").css({display:"none"});
            setTimeout(popupClose, 4000);
            $("#signupButton").css({display:"inline"})
        }
    });

}

function popupShow()
{
	$("#Popup").modal("show");
}

function popupClose()
{
    $("#Popup").modal("hide");
}

function soundcloudShow()
{
	$("#soundcloud").modal("show");
}

function soundcloudClose()
{
	$("#soundcloud").modal("hide");
}
