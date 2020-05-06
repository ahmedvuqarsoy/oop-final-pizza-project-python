document.addEventListener("DOMContentLoaded", () => {

    // order page dropdown menu functionality
    $("#id_meal").change(function () {
        $("#price").hide();
        var mealId = $(this).val();
        // if a meal is actually selected instead of the blank default value
        if (mealId != "") {
            // set various urls
            var url_meal_type = $("#orderForm").attr("data-meal_type-url");
            var url_size = $("#orderForm").attr("data-size-url");
            var url_meal_addition = $("#orderForm").attr("data-meal_addition-url");
            // once a meal is selected then send ajax request for the meal types menu
            $.ajax({
                url: url_meal_type,
                data: {
                    'meal': mealId
                },
                success: function (data) {
                    $("#id_meal_type").html(data);
                }
            });
            // reset the size menu to blank
            $.ajax({
                url: url_size,
                data: {
                    'meal_type': 0
                },
                success: function (data) {
                    $("#id_size").html(data);
                }
            });
            // reset the additions menu to blank
            $.ajax({
                url: url_meal_addition,
                data: {
                    'meal_type': 0
                },
                success: function (data) {
                    $("#id_meal_addition").html(data);
                }
            });
        }
        // if the blank default value is selected for meal, reset all menus to blank
        else {
            var url_meal_type = $("#orderForm").attr("data-meal_type-url");
            var url_size = $("#orderForm").attr("data-size-url");
            var url_meal_addition = $("#orderForm").attr("data-meal_addition-url");
            $.ajax({
                url: url_meal_type,
                data: {
                    'meal': 0
                },
                success: function (data) {
                    $("#id_meal_type").html(data);
                }
            });
            $.ajax({
                url: url_size,
                data: {
                    'meal_type': 0
                },
                success: function (data) {
                    $("#id_size").html(data);
                }
            });
            $.ajax({
                url: url_meal_addition,
                data: {
                    'meal_type': 0
                },
                success: function (data) {
                    $("#id_meal_addition").html(data);
                }
            });
        };
    });
    // once a meal type is selected then send ajax requests for the size menu and reset the additions menu
    $("#id_meal_type").change(function () {
        $("#price").hide();
        var url_size = $("#orderForm").attr("data-size-url");
        var url_meal_addition = $("#orderForm").attr("data-meal_addition-url");
        var meal_typeId = $(this).val();
        $.ajax({
            url: url_size,
            data: {
                'meal_type': meal_typeId
            },
            success: function (data) {
                $("#id_size").html(data);
            }
        });
        // reset the additions menu to blank
        $.ajax({
            url: url_meal_addition,
            data: {
                'meal_type': 0
            },
            success: function (data) {
                $("#id_meal_addition").html(data);
            }
        });
    });
    // once a size has been selected the price can be got and the add to cart button can be enabled
    $("#id_size").change(function () {
        // send ajax request for the additions menu
        var url_meal_addition = $("#orderForm").attr("data-meal_addition-url");
        $.ajax({
            url: url_meal_addition,
            data: {},
            success: function (data) {
                $("#id_meal_addition").html(data);
            }
        });
        // send ajax request for the price (not including any additions)
        $("#price").show();
        var url_price = $("#price").attr("data-price-url");
        var sizeId = $(this).val();
        $.ajax({
            url: url_price,
            data: {
                'size': sizeId
            },
            success: function (data) {
                $("#price-value").html(data);
            }
        });
        document.getElementById("add-to-cart").disabled = false;
    });
    // if any of the selected meal additions have a cost (subs) then this will be added to the price
    $("#id_meal_addition").change(function () {
        var url_price = $("#price").attr("data-price-url");
        var meal_additionId = [];
        meal_additionId.push($(this).val());
        var json_string = JSON.stringify(meal_additionId);
        $.ajax({
            url: url_price,
            traditional: true,
            data: {
                'meal_addition': json_string
            },
            success: function (data) {
                $("#price-value").html(data);
            }
        });
    });
})