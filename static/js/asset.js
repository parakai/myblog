//此函数用于checkbox的全选和反选
var checked=false;
function check_all(form) {
    var checkboxes = document.getElementById(form);
    if (checked === false) {
        checked = true;
    } else {
        checked = false;
    }
    for (var i = 0; i < checkboxes.elements.length; i++) {
        if (checkboxes.elements[i].type == "checkbox") {
            checkboxes.elements[i].checked = checked;
        }
    }
}

function checkAll(id, name){
    var checklist = document.getElementsByName(name);
    if(document.getElementById(id).checked)
        {
        for(var i=0;i<checklist.length;i++)
        {
          checklist[i].checked = 1;
        }
    }else{
        for(var j=0;j<checklist.length;j++)
        {
         checklist[j].checked = 0;
        }
    }
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function setAjaxCSRFToken() {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
var assetserver = {};
assetserver.checked = false;
assetserver.selected = {};
assetserver.language = {
    processing: "正在加载 ...",
    search: "搜索",
    select: {
        rows: {
            _:  "选中 %d 项",
            0: ""
        }
    },
    lengthMenu: "每页 _MENU_",
    info: "显示第 _START_ 至 _END_ 项结果; 共 _TOTAL_ 项",
    infoFiltered: "",
    infoEmpty: "",
    zeroRecords: "没有匹配项",
    emptyTable: "没有记录",
    paginate: {
        first: "«",
        previous: "‹",
        next: "›",
        last: "»"
    }
};

assetserver.initServerSideDataTable =function (options) {
    var ele = options.ele || $('.dataTable');
    var columnDefs = [
      // {
      //     targets: 0,
      //     orderable: false,
      //     createdCell: function (td, cellData) {
      //         $(td).html('<input type="checkbox" class="text-center ipt_check" id=99991937>'.replace('99991937', cellData));
      //     }
      // },
      {
          targets: '_all',
          className: 'text-center',
          render: $.fn.dataTable.render.text()
      }];
    columnDefs = options.columnDefs ? options.columnDefs.concat(columnDefs) : columnDefs;
    var select = {
        style: 'multi',
        selector: 'td:first-child'
    };
    var table =ele.DataTable({
        pageLength: options.pageLength || 10,
        dom: options.dom || '<"#uc.pull-left">fltr<"row m-t"<"col-md-8"<"#op.col-md-6"><"col-md-6 text-center"i>><"col-md-4"p>>',
        order: options.order || [],
        buttons: [],
        columnDefs: columnDefs,
        serverSide: true,
        processing: true,
        ajax: {
            url: options.ajax_url,
            error: function (jqXHR, textStatus, errorThrown) {
                var msg = "未知错误！";
                if (jqXHR.responseJSON) {
                    if (jqXHR.responseJSON.error) {
                        msg = jqXHR.responseJSON.error
                    } else if (jqXHR.responseJSON.msg) {
                        msg = jqXHR.responseJSON.msg
                    }
                }
                alert(msg)
            },
            data: function (data) {
                delete data.columns;
                if (data.length !== null) {
                    data.limit = data.length;
                    delete data.length;
                }
                if (data.start !== null) {
                    data.offset = data.start;
                    delete data.start;
                }
                if (data.search !== null) {
                    var search_val = data.search.value;
                    var search_list = search_val.split(" ");
                    var search_attr = {};
                    var search_raw = [];

                    search_list.map(function (val, index) {
                        var kv = val.split(":");
                        if (kv.length === 2) {
                            search_attr[kv[0]] = kv[1]
                        } else {
                            search_raw.push(kv)
                        }
                    });
                    data.search = search_raw.join("");
                    $.each(search_attr, function (k, v) {
                        data[k] = v
                    })
                }
                if (data.order !== null && data.order.length === 1) {
                    var col = data.order[0].column;
                    var order = options.columns[col].data;
                    if (data.order[0].dir === "desc") {
                        order = "-" + order;
                    }
                    data.order = order;
                }
            },
            dataFilter: function (data) {
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.count;
                json.recordsFiltered = json.count;
                return JSON.stringify(json); // return JSON string
            },
            dataSrc: "results"
        },
        columns: options.columns || [],
        select: options.select || select,
        language: assetserver.language,
        lengthMenu: [10, 20, 50, 'All'],
    });
    table.on('draw',function() {
            table.column(0, { search: 'applied', order: 'applied' }).nodes().each(function(cell, i) {
                cell.innerHTML = i + 1;
            });
    });
    return table;
}
assetserver.initDataTable = function (options) {
      var ele = options.ele || $('.dataTable');
      var columnDefs = [
          {
              targets: 0,
              orderable: false,
              createdCell: function (td, cellData) {
                  $(td).html('<input type="checkbox" class="text-center ipt_check" id=99991937>'.replace('99991937', cellData));
              }
          },
          {className: 'text-center', render: $.fn.dataTable.render.text(), targets: '_all'}
      ];
      columnDefs = options.columnDefs ? options.columnDefs.concat(columnDefs) : columnDefs;
      var select = {
                style: 'multi',
                selector: 'td:first-child'
          };
      var table = ele.DataTable({
            pageLength: options.pageLength || 15,
            dom: options.dom || '<"#uc.pull-left">flt<"row m-t"<"col-md-8"<"#op.col-md-6"><"col-md-6 text-center"i>><"col-md-4"p>>',
            order: options.order || [],
            buttons: [],
            columnDefs: columnDefs,
            ajax: {
                url: options.ajax_url,
                dataSrc: ""
            },
            columns: options.columns || [],
            select: options.select || select,
            language: assetserver.language,
            lengthMenu: [[10, 15, 25, 50, -1], [10, 15, 25, 50, "All"]]
        });
      table.on('select', function(e, dt, type, indexes) {
        var $node = table[ type ]( indexes ).nodes().to$();
        $node.find('input.ipt_check').prop('checked', true);
        assetserver.selected[$node.find('input.ipt_check').prop('id')] = true
    }).on('deselect', function(e, dt, type, indexes) {
        var $node = table[ type ]( indexes ).nodes().to$();
        $node.find('input.ipt_check').prop('checked', false);
        assetserver.selected[$node.find('input.ipt_check').prop('id')] = false
    });
    $('.ipt_check_all').on('click', function() {
      if ($(this).prop("checked")) {
          $(this).closest('table').find('.ipt_check').prop('checked', true);
          assetserver.checked = true;
          table.rows({search:'applied', page:'current'}).select();
      } else {
          $(this).closest('table').find('.ipt_check').prop('checked', false);
          assetserver.checked = false;
          table.rows({search:'applied', page:'current'}).deselect();
      }
    });
    return table;
}
function setUrlParam(url, name, value) {
    var urlArray = url.split("?");
    if (urlArray.length===1){
        url += "?" + name + "=" + value;
    } else {
        var oriParam = urlArray[1].split("&");
        var oriParamMap = {};
        $.each(oriParam, function (index, value) {
            var v = value.split("=");
            oriParamMap[v[0]] = v[1];
        });
        oriParamMap[name] = value;
        url = urlArray[0] + "?";
        var newParam = [];
        $.each(oriParamMap, function (index, value) {
            newParam.push(index + "=" + value);
        });
        url += newParam.join("&")
    }
    return url
}
function htmlEscape ( d ) {
    return typeof d === 'string' ?
        d.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;') :
        d;
}
function formSubmit(props) {
    props = props || {};
    var data = props.data || props.form.serializeObject();
    var redirect_to = props.redirect_to;
    $.ajax({
        url: props.url,
        type: props.method || 'POST',
        data: JSON.stringify(data),
        contentType: props.content_type || "application/json; charset=utf-8",
        dataType: props.data_type || "json"
    }).done(function (data, textState, jqXHR) {
        if (redirect_to) {
            location.href = redirect_to;
        } else if (typeof props.success === 'function') {
            return props.success(data, textState, jqXHR);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        if (typeof props.error === 'function') {
            return props.error(jqXHR, textStatus, errorThrown)
        }
        if (!props.form) {
            alert(jqXHR.responseText);
            return
        }
        if (jqXHR.status === 400) {
            var errors = jqXHR.responseJSON;
            var noneFieldErrorRef = props.form.children('.alert-danger');
            if (noneFieldErrorRef.length !== 1) {
                props.form.prepend('<div class="alert alert-danger" style="display: none"></div>');
                noneFieldErrorRef = props.form.children('.alert-danger');
            }
            var noneFieldErrorMsg = "";
            noneFieldErrorRef.css("display", "none");
            noneFieldErrorRef.html("");
            props.form.find(".help-block.error").html("");
            props.form.find(".form-group.has-error").removeClass("has-error");

            if (typeof errors !== "object") {
                noneFieldErrorMsg = errors;
                if (noneFieldErrorRef.length === 1) {
                    noneFieldErrorRef.css('display', 'block');
                    noneFieldErrorRef.html(noneFieldErrorMsg);
                }
                return
            }
            $.each(errors, function (k, v) {
                var fieldRef = props.form.find('input[name="' + k + '"]');
                var formGroupRef = fieldRef.parents('.form-group');
                var parentRef = fieldRef.parent();
                var helpBlockRef = parentRef.children('.help-block.error');
                if (helpBlockRef.length === 0) {
                    parentRef.append('<div class="help-block error"></div>');
                    helpBlockRef = parentRef.children('.help-block.error');
                }
                if (fieldRef.length === 1 && formGroupRef.length === 1) {
                    formGroupRef.addClass('has-error');
                    var help_msg = v.join("<br/>") ;
                    helpBlockRef.html(help_msg);
                } else {
                    noneFieldErrorMsg += v + '<br/>';
                }
            });
            if (noneFieldErrorRef.length === 1 && noneFieldErrorMsg !== '') {
                noneFieldErrorRef.css('display', 'block');
                noneFieldErrorRef.html(noneFieldErrorMsg);
            }
        }

    })
}
function APIUpdateAttr(props) {
    // props = {url: .., body: , success: , error: , method: ,}
    props = props || {};
    var user_success_message = props.success_message;
    var default_success_message = "更新成功";
    var user_fail_message = props.fail_message;
    var default_failed_message = "更新时发生未知错误";
    var flash_message = props.flash_message || true;
    if (props.flash_message === false){
        flash_message = false;
    }

    $.ajax({
        url: props.url,
        type: props.method || "PATCH",
        data: props.body,
        contentType: props.content_type || "application/json; charset=utf-8",
        dataType: props.data_type || "json"
    }).done(function(data, textStatue, jqXHR) {
        if (flash_message) {
            var msg = "";
            if (user_fail_message) {
                msg = user_success_message;
            } else {
                msg = default_success_message;
            }
            toastr.success(msg);
        }
        if (typeof props.success === 'function') {
            return props.success(data);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        if (flash_message) {
            var msg = "";
            if (user_fail_message) {
                msg = user_fail_message;
            } else if (jqXHR.responseJSON) {
                if (jqXHR.responseJSON.error) {
                    msg = jqXHR.responseJSON.error
                } else if (jqXHR.responseJSON.msg) {
                    msg = jqXHR.responseJSON.msg
                }
            }
            if (msg === "") {
                msg = default_failed_message;
            }
            toastr.error(msg);
        }
        if (typeof props.error === 'function') {
            console.log(jqXHR);
            return props.error(jqXHR.responseText, jqXHR.status);
        }
    });
  // return true;
}
// Sweet Alert for Delete
function objectDelete(obj, name, url, redirectTo) {
    function doDelete() {
        var body = {};
        var success = function() {
            if (!redirectTo) {
                $(obj).parent().parent().remove();
            } else {
                window.location.href=redirectTo;
            }
        };
        var fail = function() {
            swal("错误", "删除"+"[ "+name+" ]"+"遇到错误", "error");
        };
        APIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: 'DELETE',
            success_message: "删除成功",
            success: success,
            error: fail
        });
    }
    swal({
        title: "你确定要删除么 ？",
        text: " [" + name + "] ",
        type: "warning",
        showCancelButton: true,
        cancelButtonText: "取消",
        confirmButtonColor: "#ed5565",
        confirmButtonText: "确认",
        closeOnConfirm: true,
    }, function () {
        doDelete()
    });
}