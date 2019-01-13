function has_pre(page, city, cate) {
        if (page == '1'){
            $('.index_page').eq(0).attr('hidden', '');
            $('.pre_page').eq(0).attr('hidden', '');
        }else{
            $('.index_page').eq(0).attr({
                'onclick': "jump_to_page('1',"+ "'" + city+ "'" + "," +"'" + cate + "'" +")"
            });
            $('.index_page').eq(0).removeAttr('hidden');
            $('.pre_page').eq(0).attr({
                'onclick': "jump_to_page("+(parseInt(page)-1)+","+"'" + city+ "'" + "," +"'" + cate + "'" +")"
            });
            $('.pre_page').eq(0).removeAttr('hidden')
        }
    }

function has_next(page, city, cate) {
        var max_page = $('.ui_txt_bold04').eq(2).text();
        if(page == max_page){
            $('.next_page').eq(0).attr('hidden', '');
            $('.last_page').eq(0).attr('hidden', '');
        }else{
            $('.next_page').eq(0).attr({
                'onclick': "jump_to_page("+(parseInt(page)+1)+","+"'" + city+ "'" + "," +"'" + cate + "'" +")"
            });
            $('.next_page').eq(0).removeAttr('hidden');
            $('.last_page').eq(0).attr({
                'onclick': "jump_to_page("+ max_page+","+"'" + city+ "'" + "," +"'" + cate + "'" +")"
            });
            $('.last_page').eq(0).removeAttr('hidden');
        }
    }

function show_null(data){
        if(!data){
            return '暂无';
        }
        return data;
    }

$(function () {
        has_next('{{ page.number }}', '', '');
        has_pre('{{ page.number }}', '', '');

        $('#jumpButton').click(function () {
            jump_to_page($('#jumpNumTxt').val(), $("#currentCity").val(), $("#currentCate").val());
        });


        $("#submitQuery").click(function () {
            var select_val = $('#fyXq').val();
            if (select_val == 'city'){
                jump_to_page('1', $("#fyZldz").val());
            }else if(select_val == 'cate'){
                jump_to_page('1', '', $("#fyZldz").val());
            }
        });
    });
