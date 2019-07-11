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