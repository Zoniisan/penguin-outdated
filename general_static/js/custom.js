// table の tr に data-href 属性を追加
jQuery(function ($) {

    //data-hrefの属性を持つtrを選択しclassにclickableを付加
    $('tr[data-href]').addClass('clickable')

        //クリックイベント
        .click(function (e) {

            //e.targetはクリックした要素自体、それがa要素以外であれば
            if (!$(e.target).is('a')) {

                //その要素の先祖要素で一番近いtrの
                //data-href属性の値に書かれているURLに遷移する
                window.location = $(e.target).closest('tr').data('href');
            }
        });

});

// 文字数カウンター
function countLength(text, field) {
    document.getElementById(field).innerHTML = text.length;
}
