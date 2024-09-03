import hashlib
import multiprocessing
import getpass

# Hash functions
def hash_md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def hash_sha3_256(text: str) -> str:
    return hashlib.sha3_256(text.encode()).hexdigest()

def hash_blake2b(text: str) -> str:
    return hashlib.blake2b(text.encode()).hexdigest()

def hash_ripemd160(text: str) -> str:
    hasher = hashlib.new('ripemd160')
    hasher.update(text.encode())
    return hasher.hexdigest()

def iterative_hash(text: str, iterations: int, hash_function) -> str:
    for _ in range(iterations):
        text = hash_function(text)
    return text

def worker(chunk, iterations, hash_function):
    return iterative_hash(chunk, iterations, hash_function)

def parallel_hash(text: str, iterations: int, hash_function, num_processes: int) -> str:
    chunks = [text] * num_processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(worker, [(chunk, iterations // num_processes, hash_function) for chunk in chunks])
    
    final_result = results[0]
    for result in results[1:]:
        final_result = hash_function(final_result)
    
    return final_result

# Password verification function
def check_password(correct_password: str) -> bool:
    entered_password = getpass.getpass("Please enter your password: ")
    return entered_password == correct_password

def main():
    # Set the password (using a fixed password for development purposes)
    correct_password = "secret_password"  # Replace this with a real password
    
    # Password verification
    if not check_password(correct_password):
        print("Incorrect password. Exiting the program.")
        return
    
    # Get the text from the user
    input_text = input("Please enter the text to hash: ")
    
    num_processes = multiprocessing.cpu_count()
    
    # MD5 with 10 iterations
    intermediate_hash_md5 = parallel_hash(input_text, 10987, hash_md5, num_processes)
    
    # SHA-256 with 10 iterations
    intermediate_hash_sha256 = parallel_hash(intermediate_hash_md5, 13876780, hash_sha256, num_processes)
    
    # SHA3-256 with 30 iterations
    intermediate_hash_sha3_256 = parallel_hash(intermediate_hash_sha256, 30121, hash_sha3_256, num_processes)
    
    # BLAKE2b with 10 iterations
    intermediate_hash_blake2b = parallel_hash(intermediate_hash_sha3_256, 190780, hash_blake2b, num_processes)
    
    # RIPEMD-160 with 10 iterations
    final_hash = parallel_hash(intermediate_hash_blake2b, 100897865, hash_ripemd160, num_processes)
    
    # Print the result
    print(f"Result: {final_hash}")

if __name__ == "__main__":
    main()
