<template>
  <div class="flex h-screen">
    <!-- Left Editor Panel -->
    <div class="w-1/3 bg-gray-100 p-4 relative">
      <h2 class="text-lg font-bold mb-4">Script Editor</h2>

      <!-- Type Selection -->
      <label class="block mb-2">Select Input Type:</label>
      <select v-model="inputType" class="w-full mb-4 p-2 border rounded">
        <option value="Character">Create Character</option>
        <option value="Dialogue">Character Dialogue</option>
        <option value="Action">Action</option>
        <option value="Environment">Environment</option>
      </select>

      <!-- Character Selection (Only for Dialogue) -->
      <div v-if="inputType === 'Dialogue'" class="mb-4">
        <label class="block mb-2">Select Character:</label>
        <select v-model="selectedCharacter" class="w-full p-2 border rounded">
          <option disabled value="">Select a character</option>
          <option v-for="character in characters" :key="character" :value="character">
            {{ character }}
          </option>
        </select>
      </div>

      <!-- Fixed Size Input Field -->
      <label class="block mb-2">Enter Content:</label>
      <textarea v-model="editorContent" placeholder="Enter content..."
                class="w-full p-2 border rounded resize-none overflow-auto"
                style="height: calc(100% - 20rem);"></textarea>

      <!-- Buttons fixed at the bottom -->
      <div class="absolute bottom-4 left-4 flex space-x-4">
        <button @click="addToScript" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Confirm
        </button>
        <button @click="generateAIResponse" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
          Generate with AI
        </button>
      </div>
    </div>

    <!-- Right Script Panel -->
    <div class="w-2/3 bg-white p-4 overflow-auto">
      <h2 class="text-lg font-bold mb-4">Generated Script</h2>
      <div v-for="(line, index) in script" :key="index" class="mb-4">
        <p @dblclick="editLine(index)" v-if="editingIndex !== index">{{ line }}</p>
        <textarea v-if="editingIndex === index" v-model="script[index]" @blur="saveEdit(index)"
                  class="w-full p-2 border rounded"></textarea>
      </div>
    </div>
  </div>
</template>
<script setup>
import {ref} from "vue";

const inputType = ref("Character"); // Current input type
const editorContent = ref(""); // Universal input field content
const script = ref([]); // Script content
const characters = ref([]); // List of characters
const selectedCharacter = ref(""); // Currently selected character
const editingIndex = ref(null); // Index of the script line being edited

// Confirm Button: Add content to the script
const addToScript = () => {
  if (!editorContent.value.trim()) return;
  let newLine = "";
  if (inputType.value === "Character") {
    // Create a character
    const content = editorContent.value.trim();
    // split by '\n'
    const name = content.split('\n')[0];
    // remove name from content
    const personality = content.replace(name + '\n', '');
    generateRole(name, personality);
    characters.value.push(name);
  } else if (inputType.value === "Dialogue") {
    // Add dialogue
    if (!selectedCharacter.value) {
      alert("Please select a character first!");
      return;
    }
    newLine = `[Dialogues] ${selectedCharacter.value}: ${editorContent.value}`;
  } else if (inputType.value === "Action") {
    // Add action
    newLine = `[Action] ${editorContent.value}`;
  } else if (inputType.value === "Environment") {
    // Add environment
    newLine = `[Environment] ${editorContent.value}`;
  }

  if (inputType.value !== "Character") {
    updateInfo();
  }

  script.value.push(newLine);
  editorContent.value = ""; // Clear the input field
  if (inputType.value === "Dialogue") {
    selectedCharacter.value = ""; // Clear character selection
  }
};

const updateInfo = async () => {
  try {
    const response = await fetch("/api/updateInfo", {
      method: "POST",
      body: JSON.stringify({
        content: editorContent.value.trim(),
        info_type: inputType.value,
        character: selectedCharacter.value || "",
      }),
      headers: {"Content-Type": "application/json"},
    });
    const data = await response.json();
    if (data.success === true) {
      console.log("success to update info");
    } else {
      console.log("fail to update info");
    }
  } catch (err) {
    console.log("fail to update info", err);
  }
}

const generateRole = async (name, personality) => {
  try {
    const response = await fetch("/api/generateRole", {
      method: "POST",
      body: JSON.stringify({
        name: name,
        personality: personality
      }),
      headers: {"Content-Type": "application/json"},
    });
    const data = await response.json();
    if (data.success === true) {
      console.log("success create role");
    } else {
      console.log("fail to create role")
    }
  } catch (err) {
    console.error("Failed to generate role", err);
  }
};

// AI Generate Button: Generate content based on type
const generateAIResponse = async () => {
  if (!inputType.value) return;

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      body: JSON.stringify({
        info_type: inputType.value,
        character: selectedCharacter.value || "",
      }),
      headers: {"Content-Type": "application/json"},
    });
    const data = await response.json();
    script.value.push(data.content);
    // editorContent.value = data.content; // Fill the input field with generated content
  } catch (err) {
    console.error("Failed to generate", err);
  }
};

// Double-click to edit script
const editLine = (index) => {
  editingIndex.value = index;
};

// Save edited content
const saveEdit = (index) => {
  editingIndex.value = null;
};
</script>
