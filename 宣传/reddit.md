**Loong: A Programming Language to Enhance Human-AI Collaboration**

Loong (working title) is an attempt to improve the interaction between developers and generative AI. While Python is widely used in AI development, there are certain limitations that hinder intuitive collaboration with AI. Loong is designed to address these challenges by focusing on clarity and structure, making collaboration between humans and AI more seamless.

### **Design Philosophy of Loong:**

#### 1. **Intuitive Syntax Order**
Loong aims to make the syntax more reflective of the actual execution order of a program, reducing the need for complex abstractions. Unlike Python's list comprehensions, Loong’s syntax is designed to be more intuitive, making code easier to read and generate for both humans and AI.

**Mapping and Filtering Example:**
```loong
let numbers = [1, 2, 3, 4];
let doubled = numbers @ [x => x * 2];  // Doubles each number in the list
let filtered = numbers >? [x => x > 2];  // Filters numbers greater than 2
```

#### 2. **Improved Closure Semantics**
Loong improves closure handling by simplifying lexical scoping, making it easier for both developers and AI systems to understand the context.

#### 3. **Eliminating Indentation Dependency**
Unlike Python, Loong does not rely on indentation for code blocks, instead using explicit block markers like `end`. This makes it easier to avoid indentation errors, especially when copying and pasting code.

**Function Definition and Invocation Example:**
```loong
fun sum(x, y):
    x + y
end

let result = sum(10, 20);
```

### **Key Features of Loong:**
- **Concise Variable Definitions**: Use `let` to quickly declare variables.  
- **Ternary Operators**: Straightforward conditional expressions.  
- **Advanced Data Types**: Built-in support for arrays and dictionaries.  
- **Anonymous Functions and Closures**: Support for concise expressions like `x => x + 1`.  
- **Collection Operations**: Convenient mapping and filtering with `@` and `>?` operators.

### **Seamless Interoperability with Python**
Loong integrates seamlessly with Python, enabling developers to leverage Python's vast ecosystem while benefiting from Loong's simplified syntax.

### **Optimized for Generative AI**
Loong is designed with generative AI in mind. Its simple and clear structure makes it easier for AI to understand and generate code, fostering more effective collaboration between humans and machines.

---

### **Get Started with Loong**
Loong is still in active development, with basic features already available. If you're curious, feel free to give it a try!  
**GitHub Repository: [https://github.com/picasso250/loong-lang](https://github.com/picasso250/loong-lang)**

#### **Installation and Execution**

Run the following command to start the Loong interpreter:

```bash
pip install lark colorama termcolor
python loong.py
```

#### **Run Tests**
```bash
python test_loong.py
```

---

### **Join Our Community**
Loong is open to contributions from developers and AI enthusiasts alike. Contribute feedback or code to help improve Loong by visiting our GitHub!
