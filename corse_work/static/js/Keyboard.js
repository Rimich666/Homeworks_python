class Keyboard {
    elements = {
        main: null,
        keysContainer: null,
        keys: []
    }

    eventHandlers = {
        oninput: null,
        onclose: null
    }

    properties = {
        value: "",
        capsLock: false,
        element_id: null,
        parent_id: "",
        key_done: 'done',
        input_class: ".use-keyboard-input",
        id_done: "add_shopping_button"
    }

    init() {
        // Create main elements
        let par = document.getElementById(this.properties.parent_id);
        this.elements.main = document.createElement("div");
        this.elements.keysContainer_l = document.createElement("div");
        this.elements.keysContainer_r = document.createElement("div");

        // Setup main elements
        this.elements.main.classList.add("keyboard", "keyboard--hidden");
        this.elements.main.id = 'keyboard_' + this.properties.key_done;
        this.elements.keysContainer_l.classList.add("keyboard__keys" ,"keyboard__keys--l");
        this.elements.keysContainer_r.classList.add("keyboard__keys" ,"keyboard__keys--r");
        this.elements.keysContainer_l.appendChild(this._createKeys(["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", "." ]));
        this.elements.keysContainer_r.appendChild(this._createKeys(["backspace", this.properties.key_done]));
    
        // Add to DOM
        this.elements.main.appendChild(this.elements.keysContainer_l);
        this.elements.main.appendChild(this.elements.keysContainer_r);
        par.appendChild(this.elements.main);
    //    document.body.appendChild(this.elements.main);


        // Automatically use keyboard for elements with .use-keyboard-input
        this.link_elements();
    }

    link_elements(){
        // Automatically use keyboard for elements with .use-keyboard-input
        document.querySelectorAll(this.properties.input_class).forEach(element => {
             element.addEventListener("focus", () => {
                let top = $(element).offset().top + $(element).outerHeight();
                $(this.elements.main).offset({top: top, left: $(element).offset().left});
                this.properties.element_id = element.id;
                this.open(element.value, currentValue => {
                    element.value = currentValue;
                });
            });
        });
    }

    _createKeys(keyLayout) {
        const fragment = document.createDocumentFragment();
        // Creates HTML for an icon
        const createIconHTML = (icon_name) => {
            return `<i class="material-icons">${icon_name}</i>`;
        };

        keyLayout.forEach(key => {
            const keyElement = document.createElement("button");
            const insertLineBreak = ["backspace", "9", "3", "6"].indexOf(key) !== -1;

            // Add attributes/classes
            keyElement.setAttribute("type", "button");
            keyElement.classList.add("keyboard__key");

            switch (key) {

                case "backspace":
                    keyElement.classList.add("keyboard__key--high");
                    keyElement.innerHTML = createIconHTML("backspace");

                    keyElement.addEventListener("click", () => {
                        this.properties.value = this.properties.value.substring(0, this.properties.value.length - 1);
                        this._triggerEvent("oninput");
                    });

                    break;

                case (this.properties.key_done):
                    keyElement.classList.add("keyboard__key--high", "keyboard__key--dark");

                    keyElement.innerHTML = createIconHTML(this.properties.key_done);
                    keyElement.id = this.properties.id_done;
                    keyElement.addEventListener("click", () => {
                        this.close();
                        this._triggerEvent("onclose");
                    });

                    break;
                case "0":
                    keyElement.classList.add("keyboard__key--widest");
                    keyElement.textContent = key; 
                    keyElement.addEventListener("click", () => {
                    this.properties.value += key;
                    this._triggerEvent("oninput");
                    });
    
                    break;
                default:
                    keyElement.textContent = key.toUpperCase();
                    keyElement.addEventListener("click", () => {
                        this.properties.value += key;
                        this._triggerEvent("oninput");
                    });

                    break;
            }

            fragment.appendChild(keyElement);

            if (insertLineBreak) {
                fragment.appendChild(document.createElement("br"));
            }
        });

        return fragment;
    }

    _triggerEvent(handlerName) {
        if (typeof this.eventHandlers[handlerName] == "function") {
            this.eventHandlers[handlerName](this.properties.value);
        }
    }


    open(initialValue, oninput, onclose) {
        console.log(typeof oninput);
        this.properties.value = initialValue || "";
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.remove("keyboard--hidden");
    }

    close() {
        this.properties.value = "";
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.add("keyboard--hidden");
        let keyb = $(this.elements.main);
        keyb.offset({top:0, left:-keyb.width()})
    }
}
