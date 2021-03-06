document.addEventListener("DOMContentLoaded", function() {

getInstitutions(1, 1);


  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
        console.log(this.currentSlide);
        getInstitutions(this.currentSlide, 1)
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;
      let active_slide = document.querySelector(".help--slides.active")
      let type = active_slide.dataset.id;
      getInstitutions(type, page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();

          if (this.currentStep === 2) {
            let step = document.querySelector("div[data-step='3']");
            const button_div = step.querySelector(".form-group--buttons")
            let categories = document.querySelectorAll('input[name="categories"]:checked');
            let params = ""
            for (let el of categories) {
              params = params+ 'cat_ids=' + el.value + "&"
            }
            let addres = "/get_institutions/?" + params;

            fetch(addres, {method: 'GET',})
                .then((res) => {
              return res.json();
            })
                .then((res) => {
                    console.log(res);
                  let existing_checkboxes =  step.querySelectorAll(".form-group--checkbox");
                  if (existing_checkboxes !== null) {
                      for (let checkbox of existing_checkboxes) {
                          checkbox.remove()
                      }
                  };
                  for (let org of res.institutions) {
                    const div = document.createElement("div");

                    div.classList.add("form-group", "form-group--checkbox");
                    div.innerHTML += `
                    <label>
                    <input type="radio" name="organization" value="${org.id}" />
                    <span class="checkbox radio"></span>
                    <span class="description">
                      <div class="title">${org.type} “${org.name}”</div>
                      <div class="subtitle">
                        Cel i misja: ${org.description}
                      </div>
                    </span>
                    </label>
                    `;
                    step.insertBefore(div, button_div);
                  }
            })
          }
          if (this.currentStep === 4) {
            let step_5 = document.querySelector("div[data-step='5']");
            if (step_5.children.length === 3) {
              step_5.children[1].remove()
            }
            let step_5_buttons = step_5.querySelector(".form-group--buttons")

            let picked_categories = document.querySelectorAll('input[name="categories"]:checked');
            let categories = ""
             for (let el of picked_categories) {
              categories += el.nextElementSibling.nextElementSibling.innerHTML + " ";
            }
            let bags_quantity = document.querySelector('input[name="bags"]');

            let picked_organization = document.querySelector('input[name="organization"]:checked');
            let organization = picked_organization.nextElementSibling.nextElementSibling.firstElementChild.innerHTML

            let step_4 = document.querySelector("div[data-step='4']");
            let address = step_4.querySelector('input[name="address"]');
            let city = step_4.querySelector('input[name="city"]');
            let postcode = step_4.querySelector('input[name="postcode"]');
            let phone = step_4.querySelector('input[name="phone"]');
            let data = step_4.querySelector('input[name="data"]');
            let time = step_4.querySelector('input[name="time"]');
            let more_info = step_4.getElementsByTagName('textarea')[0];
            if (more_info.value === "") {
              more_info.value = "Brak uwag"
            }

            let div = document.createElement("div");
            div.classList.add("summary")
            div.innerHTML = `
              <div class="form-section">
                <h4>Oddajesz:</h4>
                <ul>
                  <li>
                    <span class="icon icon-bag"></span>
                    <span class="summary--text">
                        ${bags_quantity.value} x worek ${categories}
                    </span>
                  </li>
                  <li>
                    <span class="icon icon-hand"></span>
                    <span class="summary--text"
                      >Dla ${organization}</span
                    >
                  </li>
                </ul>
              </div>
              <div class="form-section form-section--columns">
                <div class="form-section--column">
                  <h4>Adres odbioru:</h4>
                  <ul>
                    <li>${address.value}</li>
                    <li>${city.value}</li>
                    <li>${postcode.value}</li>
                    <li>${phone.value}</li>
                  </ul>
                </div>
                <div class="form-section--column">
                  <h4>Termin odbioru:</h4>
                  <ul>
                    <li>${data.value}</li>
                    <li>${time.value}</li>
                    <li>${more_info.value}</li>
                  </ul>
                </div>
              </div>`
            step_5.insertBefore(div, step_5_buttons);
          }
              this.currentStep++;
              this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      var valid = true
      let bags_quantity = document.querySelector('input[name="bags"]');
      let picked_categories = document.querySelectorAll('input[name="categories"]:checked');
      let categories = [];
       for (let el of picked_categories) {
        categories.push(el.value)
      }
      let organization = document.querySelector('input[name="organization"]:checked');
      let step_4 = document.querySelector("div[data-step='4']");
      let address = step_4.querySelector('input[name="address"]');
      let phone = step_4.querySelector('input[name="phone"]');
      let city = step_4.querySelector('input[name="city"]');
      let postcode = step_4.querySelector('input[name="postcode"]');
      let data = step_4.querySelector('input[name="data"]');
      let time = step_4.querySelector('input[name="time"]');
      let more_info = step_4.getElementsByTagName('textarea')[0];

      fetch('/add-donation/',
          {
            method: 'POST',
            headers: {
              "Content-type": "application/json",
              "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({'quantity': bags_quantity.value,
                                        'categories': categories,
                                        'institution': organization.value,
                                        'address': address.value,
                                        'phone_number': phone.value,
                                        'city': city.value,
                                        'zip_code': postcode.value,
                                        'pick_up_date': data.value,
                                        'pick_up_time': time.value,
                                        'pick_up_comment': more_info.value,
                                        })
          })
                .then((res) => {
              return res.json();
              })
                .then((res) => {
              if (Object.keys(res.errors).length !== 0) {
                valid = false
                let step_1 = document.querySelector("div[data-step='1']");
                let error_ul = step_1.querySelector(".error")
                if (error_ul !== null) {
                  step_1.children[0].remove()
                }
                let h3 = step_1.querySelector("h3");
                let ul = document.createElement("ul");
                ul.classList.add("form--steps-counter", "error")
                for (let el in res.errors) {
                  let li = document.createElement("li")
                  li.innerHTML = res.errors[el].error;
                  ul.appendChild(li)
                }
                step_1.insertBefore(ul, h3);
                this.currentStep = 1;
                this.updateForm();
              }
              let form = document.querySelector("form")
              if (valid) form.submit()
        })

    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});

function getCookie(c_name) {
        if(document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if(c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if(c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }

function getInstitutions(type, page) {
    let addres = "/institutions/?" + "type=" + type + "&page=" + page;
    fetch(addres, {method: 'GET'})
        .then((res) => {
      return res.json();
    })
        .then((res) => {
          let active_div = document.querySelector(".help--slides.active");
          active_div.innerHTML = "";
          let paragraph = document.createElement("p");
          paragraph.innerHTML = "W naszej bazie znajdziesz listę zweryfikowanych fundacji, organizacji pozarzadowych i lokalnych zbiórek, z którymi współpracujemy. Możesz sprawdzić czym się zajmują, komu pomagają i czego potrzebują.";
          active_div.appendChild(paragraph);
          let element_list = document.createElement("ul");
          element_list.classList.add("help--slides-items");

          for (let el of res.institutions) {
            let categories = "";
            for(let cat of el.categories) {
              categories = categories + cat.name + " "
            }
            element_list.innerHTML += `
                  <li>
                  <div class="col">
                  <div class="title">${el.name}</div>
                  <div class="subtitle">Cel i misja: ${el.description}</div>
                  </div>
                  <div class="col"><div class="text">
                  ${categories}
                  </div></div>
              </li>
            `
          }
          active_div.appendChild(element_list);

          let page_list = document.createElement("ul");
          page_list.classList.add("help--slides-pagination");

          for (let i=1; i<= res.last_page; i++) {
            page_list.innerHTML += `
            <li><a href="#" class="btn btn--small btn--without-border" data-page="${i}">${i}</a></li>
            `
          }
          active_div.appendChild(page_list);
          for (let li of page_list.children) {
            li.firstElementChild.classList.remove("active");
          }
          let active_page = page_list.querySelector("a[data-page='" + page + "']");
          active_page.classList.add("active");

    })
};
