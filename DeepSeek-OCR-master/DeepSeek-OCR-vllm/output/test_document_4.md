<|ref|>text<|/ref|><|det|>[[211, 35, 927, 150]]<|/det|>
and searching for an element. The following example implements collection _type as an opaque type, hiding the implementation details of the data type from the library's user. To accomplish this, we create two header files: an external collection.h header file included by the user of the data type, and an internal file included only in files that implement the functionality of the data type.  

<|ref|>text<|/ref|><|det|>[[211, 150, 927, 189]]<|/det|>
In the external collection.h header file, the collection_type data type is defined as an instance of struct collection_type, which is an incomplete type:  

<|ref|>text<|/ref|><|det|>[[58, 204, 491, 355]]<|/det|>
typedef struct collection_type collection_type; // Function declarations extern error_t create_collection(collection_type \*\*result); extern void destroy_collection(collection_type \*col); extern error_t add_to_collection(collection_type \*col, const void \*data, size_t byteCount); extern error_t remove_from_collection(collection_type \*col, const void \*data, size_t byteCount); extern error_t find_in_collection(const collection_type \*col, const void \*data, size_t byteCount); //- - - snip- - -  

<|ref|>text<|/ref|><|det|>[[211, 374, 904, 450]]<|/det|>
The collection_type identifier is aliased to struct collection_type (an incomplete type). Consequently, functions in the public interface must accept a pointer to this type, instead of an actual value type, because of the constraints placed on the use of incomplete types in C.  

<|ref|>text<|/ref|><|det|>[[211, 450, 928, 488]]<|/det|>
In the internal header file, struct collection_type is fully defined but not visible to a user of the data abstraction:  

<|ref|>text<|/ref|><|det|>[[211, 504, 441, 650]]<|/det|>
struct node_type { void \*data; size_t size; struct node_type \*next; }; struct collection_type { size_t num_elements; struct node_type \*head; };  

<|ref|>text<|/ref|><|det|>[[211, 692, 916, 769]]<|/det|>
Modules that implement the abstract data type include both the external and internal definitions, whereas users of the data abstraction include only the external collection.h file. This allows the implementation of the collection_type data type to remain private.  

<|ref|>sub_title<|/ref|><|det|>[[97, 801, 264, 824]]<|/det|>
## Executables  

<|ref|>text<|/ref|><|det|>[[211, 833, 916, 949]]<|/det|>
In Chapter 9, you learned that the compiler is a pipeline of translation phases, and that the compiler's ultimate output is object code. The last phase of translation, called the link phase, takes the object code for all of the translation units in the program and links it together to form a final executable. This can be an executable that a user can run, such as a.out or foo.exe, a library, or a more specialized program such as a device driver