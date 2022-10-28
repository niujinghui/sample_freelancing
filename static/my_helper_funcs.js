console.log("start executing my_helper_funcs.js!");

document.addEventListener("DOMContentLoaded", function(event) {
    console.log("DOM fully loaded and parsed, DOM完全加载并分析完毕！");
});





const canvas_for_measuring = document.createElement("canvas");



// 我自己常用的helper functions:
const MyHelpers = {

    calculateTextWidth: function(text, inside_elm) {
        let context = canvas_for_measuring.getContext("2d");
        context.font = getComputedStyle(inside_elm).font;
        let metrics = context.measureText(text);
        return metrics.width;
    },

    debounce: function(func, wait_time) {
        let timeout;
        return function() {
            let context = this,
                args = arguments;
            let later = function() {
                func.apply(context, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait_time || 200);
        };
    },

    containUppercase: function(test_string) {
        if (test_string == test_string.toLowerCase()) {
            return false;
        }
        else {
            return true;
        }
    },

    promisified_blink: function(elem, times, speed) {
        console.log(`promisified_blink函数开始运行! times: ${times},  speed: ${speed}`);
        times = parseInt(times, 10) || 3; // 确保是整数。
        speed = speed || 100;
        let previous_color = elem.style.color;
        let returned_promise = Promise.resolve();
        let delayed_blink_once = function(resolved_value) {
            return new Promise(function(resolve, reject) {
                setTimeout(function() {
                    console.log("doing blinking once...");
                    if (elem.style.color === "red") {
                        elem.style.color = "";
                    }
                    else {
                        elem.style.color = "red";
                    }
                    resolve();
                }, speed);
            });
        }
        if (times < 0) { // "times<0"的情况下会无限闪烁下去。
            setInterval(function() {
                // console.log("doing blinking once...");
                if (elem.style.color === "red") {
                    elem.style.color = "";
                }
                else {
                    elem.style.color = "red";
                }
            }, speed);
            return;
        }
        while (times > 0) { // "times>0"的情况，有次数限制。
            console.log("bury a delayed blink...");
            returned_promise = returned_promise.then(delayed_blink_once);
            times -= .5;
        }
        console.log(`promisified_blink函数运行完毕! times: ${times},  speed: ${speed}`);
        return returned_promise.then(e => elem.style.color = previous_color);
    },

    delay: function(ms) {
        var ctr, rej, p = new Promise(function(resolve, reject) {
            // console.log(`程序延迟 ${ms} 豪秒 ......`);
            ctr = setTimeout(function() {
                // console.log(`所延迟的${ms}毫秒结束，程序继续运行...`);
                resolve();
            }, ms);
            rej = reject;
        });
        p.cancel = function() {
            clearTimeout(ctr);
            rej(Error("Cancelled"))
        };
        return p;
    },

    assert: function(condition, message) {
        if (!condition) {
            throw new Error(message || "Assertion failed");
        }
    },

    // Handle for browsers without HTML5 constraint validation turned on.
    validateForm: function(form) {
        let invalidFields;

        form.find(".ui-state-error-text")
            .removeClass("ui-state-error-text")
        form.find("[aria-invalid]").attr("aria-invalid", false)
        form.find(":ui-tooltip").tooltip("destroy");

        invalidFields = form.find(":invalid").each(function() {
            form.find("label[for=" + this.id + "]")
                .addClass("ui-state-error-text")
            $(this).attr("aria-invalid", true)
                .attr("title", this.validationMessage)
                .tooltip({
                    tooltipClass: "ui-state-error"
                });
        }).first().focus();

        return invalidFields.length === 0;
    },

    castType: function(value) {
        if (typeof value == "string") {
            value = value.trim();
        }
        if (value === "undefined") return undefined;
        if (value === "null") return null;
        if (value === "") return null;
        if (value === null) return null;
        if (value === "true") return true;
        if (value === "false") return false;
        var v = Number(value);
        return isNaN(v) ? value : v;
    },

    catch_event_in_bubblePath: function({ event, target_selector }) {
        /*
            event.currentTarget是 event_handler 所贴的element.
            event.target是鼠标点击的地方
            两者之间的bubble路径中只要含有<target_selector>,就要进行处理。
        */
        const bubble_start = event.target,
            bubble_end = event.currentTarget;
        let node = bubble_start;
        while (node != bubble_end && node != document) {
            if (node.matches(target_selector)) {
                return node;
            }
            node = node.parentNode;
        }
        //如果能执行到这一步的话，说明点歪了。
        // console.log(`${event.type}虽然发生，但是路径不包含${target_selector}！路径发生在了：${event.target}`);
    },

    request_backend: function(url, params_to_backend) {
        const final_params_obj = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };
        if (params_to_backend && params_to_backend.constructor.name === "FormData") {
            params_to_backend = Object.fromEntries(params_to_backend);
            // cast type:
            Object.keys(params_to_backend).forEach(k => { params_to_backend[k] = MyHelpers.castType(params_to_backend[k]) });
        }
        // request "body":
        final_params_obj["body"] = JSON.stringify(params_to_backend);
        return fetch(url, final_params_obj)
            .then(response => {
                if (response.ok) {
                    const result = response.json();
                    result.then(r => console.log(`Successfully retrieved from <${url}> :`, r));
                    return result;
                }
                else {
                    console.log(`request_backend <${url}>遇到了错误：`, response.statusText);
                    throw Error(response.statusText);
                }
            });
    }
};

export { MyHelpers };


console.log("end executing my_helper_funcs.js!");
