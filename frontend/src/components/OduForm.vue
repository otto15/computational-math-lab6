<template>
  <div class="container">
    <div class="function-form">
      <div class="form-group">
        <label for="functionInput">Function</label>
        <select id="functionInput" class="form-control" v-model="func">
          <option v-for="(func, i) in functions" :key="i" :value="func">
            {{ func.string_rep }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="x0">X_0</label>
        <input ref="x0" id="x0" type="number" class="form-control" v-model="x0"/>
        <div v-if="errorMessages['x0']" class="error-message">{{ errorMessages['x0'] }}</div>
      </div>
      <div class="form-group">
        <label for="y0">Y_0</label>
        <input ref="y0" id="y0" type="number" class="form-control" v-model="y0"/>
        <div v-if="errorMessages['y0']" class="error-message">{{ errorMessages['y0'] }}</div>
      </div>
      <div class="form-group">
        <label for="intervalLength">Length of interval</label>
        <input ref="intervalLength" id="intervalLength" type="number" class="form-control" v-model="intervalLength"/>
        <div v-if="errorMessages['intervalLength']" class="error-message">{{ errorMessages['intervalLength'] }}</div>
      </div>
      <div class="form-group">
        <label for="step">Step</label>
        <input ref="step" type="number" id="step" class="form-control" v-model="step">
        <div v-if="errorMessages['step']" class="error-message">{{ errorMessages['step'] }}</div>
      </div>
      <div class="form-group">
        <label for="accuracy">Accuracy</label>
        <input ref="accuracy" type="number" id="step" class="form-control" v-model="accuracy">
        <div v-if="errorMessages['accuracy']" class="error-message">{{ errorMessages['accuracy'] }}</div>
      </div>
    </div>
    <div class="buttons-container">
      <button :title="errorMessage" @click="sendOdu" class="send-btn">
        Solve
      </button>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      func: 'Math.exp(x)',
      x0: '',
      y0: '',
      errorMessages: {},
      errorMessage: '',
      functions: [],
      intervalLength: '',
      step: '',
      accuracy: ''
    };
  },
  mounted() {
    axios
        .get(import.meta.env.VITE_BACKEND_URL + "/odu")
        .then(response => {
          console.log(response.data);
          this.functions = response.data;
          this.func = response.data[0];
        })
        .catch(() => {
          this.errorMessage = 'Error sending points to server';
        });
  },
  methods: {
    isValid() {
      let s = "All fields must not be empty";
      if (this.x0 === '') {
        this.errorMessage = s;
      }

      if (this.y0 === '') {
        this.errorMessage = s;
      }

      if (this.intervalLength === '') {
        this.errorMessage = s;
      } else {
        if (this.intervalLength <= 0) {
          this.errorMessages['intervalLength'] = "Interval length must be positive";
          this.errorMessage = "Fix errors above, please";
        }
      }

      if (this.step === '') {
        this.errorMessage = s;
      } else {
        if (this.step <= 0) {
          this.errorMessages['step'] = "Step must be positive";
          this.errorMessage = "Fix errors above, please";
        }
      }

      if (this.accuracy === '') {
        this.errorMessage = s;
      } else {
        if (this.accuracy <= 0) {
          this.errorMessages['accuracy'] = "Accuracy must be positive";
          this.errorMessage = "Fix errors above, please";
        }
      }

      return this.errorMessage === '';
    },
    sendOdu() {
      this.errorMessages = {};
      this.errorMessage = '';
      if (this.isValid()) {
        axios
            .post(import.meta.env.VITE_BACKEND_URL + "/odu", {
              equation_id: this.func.equation_id,
              x_0: this.x0,
              y_0: this.y0,
              length: this.intervalLength,
              h: this.step,
              e: this.accuracy
            })
            .then(response => {
              console.log(response.data);
            })
            .catch(() => {
              this.errorMessage = 'Error sending points to server';
            });
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.buttons-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1rem;
}

.send-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #4caf50;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: default;
}

.send-btn {
  background-color: #2196f3;
}

.send-btn:hover {
  background-color: #0673c0;
}

.error-message {
  margin-top: 1rem;
  padding: 0.5rem;
  border: 1px solid #f44336;
  background-color: #ffebee;
  color: #f44336;
  font-size: 0.8rem;
  text-align: center;
  width: 100%;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  /* display: none; <- Crashes Chrome on hover */
  -webkit-appearance: none;
  margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
}

.file-upload input[type="file"] {
  display: none;
}

.function-form {
  max-width: 400px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

</style>