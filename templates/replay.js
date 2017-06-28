/**
 * Created by amr on 27/06/17.
 */
$(document).ready(function () {
      $(".comment-reply-btn").click(function (event) {
          event.preventDefault();
          $(this).parent().next(".comment-reply").fadeToggle();
      });
      // $("#following").hover(function(){
      //
      //       // $(".unfollow").show();
      //   },
      //   function(){
      //     $(this).show();
      //       // $(".unfollow").hide();
      //   });

});