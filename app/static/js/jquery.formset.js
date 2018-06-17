(function ($) {
    var updateElementIndex = function(el, prefix, ndx) {
        var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
        var replacement = prefix + "-" + ndx;
        if ($(el).attr("for")) {
            $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        }
        if (el.id) {
            el.id = el.id.replace(id_regex, replacement);
        }
        if (el.name) {
            el.name = el.name.replace(id_regex, replacement);
        }
    };

    /**
     * Will handle the 'add another' feature.
     *
     * This plugin should be applied to a container containing a 'add another'
     * link, the management form of the formset and an empty template (with
     * css class ``empty``).
     *
     * Required options:
     *   prefix
     */
    $.fn.formset = function (opts) {
        return $(this).each(function () {
            var template = $(this).find('.empty');
            $('#add_' + opts.prefix + '_form').click(function () {
                var form = template.clone(),
                    total_forms_input = $('#id_' + opts.prefix + '-TOTAL_FORMS');
                    total_forms = parseInt(total_forms_input.val());
                form.find('.' + opts.prefix + '-count').text(total_forms + 1);
                form.find('*').each(function () {
                    updateElementIndex(this, opts.prefix, total_forms);
                });
                template.before(form);
                total_forms_input.val(total_forms + 1);
                form.show();
            });
        });
    };
})(jQuery);
