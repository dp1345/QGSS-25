def find_best_metrics(backend: QiskitRuntimeService.backend) -> list[tuple[int or list, float]]:
    """Finds the best-performing qubits and qubit pair based on various hardware metrics."""
    
    #---- TODO : Task 0 ---
    #Define metrics lists for the backend
    t1, t2, gate_error_x, readout_error, gate_error_ecr = [], [], [], [], []
    num_qubits = backend.num_qubits
    properties = backend.properties()
    coupling_map = backend.coupling_map

    # define various lists of metrics for all the qubits of the backend
    for i in range(num_qubits):
        t1.append(properties.t1(i))
        t2.append(properties.t2(i))
        gate_error_x.append(properties.gate_error(gate="x", qubits=i))
        readout_error.append(properties.readout_error(i))

    for pair in coupling_map:
        gate_error_ecr.append(properties.gate_error(gate="ecr", qubits=pair))
        
    # ---- TODO : Task 1 ---
    # Goal: Obtain the best value and the index or indices of the qubits of the following metrics:

    #find the best qubit (index_t1_max) with the longest T1 and its value (max_t1)
    max_t1 = max(t1)
    index_t1_max = t1.index(max_t1)

    #find the best qubit (index_t2_max) with the longest T2 and its value (max_t2)
    max_t2 = max(t2)
    index_t2_max = t2.index(max_t2)

    #find the best qubit (index_min_x_error) with the smallest x gate error and its value (min_x_error)
    min_x_error = min(gate_error_x)
    index_min_x_error = gate_error_x.index(min_x_error)

    #find the best qubit (index_min_readout) with the smallest readout error and its value (min_readout)
    min_readout = min(readout_error)
    index_min_readout = readout_error.index(min_readout)

    #find the best qubit pairs with minimum ecr error (min_ecr_pair) and its value (min_ecr_error)
    coupling_list = coupling_map.get_edges()
    min_ecr_error = min(gate_error_ecr)
    min_ecr_index = gate_error_ecr.index(min_ecr_error)
    min_ecr_pair = coupling_list[min_ecr_index]
    
    # --- End of TODO ---

    solutions = [
        [int(index_t1_max), max_t1],
        [int(index_t2_max), max_t2],
        [int(index_min_x_error), min_x_error],
        [int(index_min_readout), min_readout],
        [list(min_ecr_pair), min_ecr_error],
    ]
    return solutions



# pauli
num_nodes = graph.num_nodes()
    identity_weight = 0.5 * len(graph.edge_list())

    for (i, j) in graph.edge_list():
        z_pauli = ['I'] * num_nodes
        z_pauli[i] = 'Z'
        z_pauli[j] = 'Z'
        pauli_word = ''.join(z_pauli)
        pauli_list.append((pauli_word, -0.5))

    pauli_list.append(('I' * num_nodes, identity_weight))


         # ---- TODO : Task 5 ---
        # Goal: Find the transpiler seed that minimizes two-qubit gate error for a given circuit and backend looping from 0 to 500

        # TODO Use the `two_qubit_gate_errors_per_circuit_layout` function to count for the error of the transpile circuit
        result = two_qubit_gate_errors_per_circuit_layout(circuit_opt_seed, backend)
        err_acc = result[0]
        twoq_gate_count = result[1]
        # TODO Check if the error accounted above is smaller than min_err_acc_seed_loop. If so, assign the variables that this function returns
        if err_acc < min_err_acc_seed_loop:
            min_err_acc_seed_loop = err_acc
            best_seed_transpiler = seed_transpiler
            circuit_opt_best_seed = circuit_opt_seed
            two_qubit_gate_count_seed_loop = twoq_gate_count


def fold_local_circuit(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """Performs Zero-Noise Folding at the level of individual circuit instructions."""

    if scale_factor % 2 == 0:
        raise ValueError("scale must be an odd positive integer (1, 3, 5, ...)")
    # We define the number of times we are going to "fold" each instruction
    n_repeat = (scale_factor - 1) // 2
    qc_folded = QuantumCircuit(circuit.qubits, circuit.clbits)

    if scale_factor == 1:
        return circuit
    else:
        for instrction in circuit.data:
        # ---- TODO : Task 6b ---
        # Implement the local circuit folding. Don't fold measurement gates!
           instr, qargs, cargs = instrction
           if instr.name == "measure":
               qc_folded.append(instr, qargs, cargs)
           else:
               qc_folded.append(instr, qargs, cargs)
               for _ in range(n_repeat):
                  qc_folded.append(instr.inverse(), qargs, cargs)
                  qc_folded.append(instr, qargs, cargs)
             

        # --- End of TODO ---

    return qc_folded