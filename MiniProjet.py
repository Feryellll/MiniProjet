from ortools.sat.python import cp_model


class MySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, assignment, instructors, rooms, exams, solution_limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._assignment = assignment
        self._instructors = instructors
        self._rooms = rooms
        self._exams = exams
        self._solution_count = 0
        self._solution_limit = solution_limit

    def on_solution_callback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for i in range(len(self._instructors)):
            for e in range(len(self._exams)):
                for r in range(len(self._rooms)):
                    if self.Value(self._assignment[(i, e, r)]):
                        instructor_name = self._instructors[i]
                        exam_name = self._exams[e]
                        room_name = self._rooms[r]
                        print(f"Instructor: {instructor_name}, Exam: {exam_name}, Room: {room_name}.")
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self._solution_count


def main():
    
    instructors = ['PROF1', 'PROF2', 'PROF3', 'PROF4', 'PROF5']
    rooms = ['ROOM1', 'ROOM2', 'ROOM3', 'ROOM4', 'ROOM5']
    exams = ['CLOUD', 'SPRINGBOOT', 'PARADIGME', 'IA', 'DEVOPS']

    all_instructors = range(len(instructors))
    all_rooms = range(len(rooms))
    all_exams = range(len(exams))

    model = cp_model.CpModel()

    assignment = {}

    for i in all_instructors:
        for e in all_exams:
            for r in all_rooms:
                assignment[(i, e, r)] = model.NewBoolVar(
                    f"i{i}_e{e}_r{r}")

    for e in all_exams:
        model.Add(sum(assignment[(i, e, r)] for i in all_instructors for r in all_rooms) == 1)

    for r in all_rooms:
        model.Add(sum(assignment[(i, e, r)] for i in all_instructors for e in all_exams) == 1)
    solver = cp_model.CpSolver()

    solution_limit = 5
    solution_printer = MySolutionPrinter(
        assignment, instructors, rooms, exams, solution_limit
    )

    solver.Solve(model, solution_printer)


if __name__ == "__main__":
    main()
