from flask import jsonify, request, render_template
from src.models.student import Student
from config.db import SessionLocal
from flasgger import Swagger
import design

def init_api_routes(app):
    swagger = Swagger(app)  # Inicializar Swagger en la aplicación Flask

    @app.route('/student_list')
    def show_student_list():
        return render_template('pagina_principal.html')

    @app.route('/api/students', methods=['GET'])
    def get_students():
        """
        Get all students.

        ---
        responses:
          200:
            description: A list of students.
            schema:
              id: Students
              properties:
                students:
                  type: array
                  items:
                    $ref: '#/definitions/Student'
          404:
            description: No students found.
        """
        session = SessionLocal()
        students = session.query(Student).all()
        session.close()
        return jsonify([student.serialize() for student in students])

    @app.route('/api/students/<int:student_id>', methods=['GET'])
    def get_student_by_id(student_id):
        """
        Get a student by ID.

        ---
        parameters:
          - name: student_id
            in: path
            description: ID of the student to retrieve
            required: true
            type: integer
        responses:
          200:
            description: Student found.
            schema:
              $ref: '#/definitions/Student'
          404:
            description: Student not found.
        """
        session = SessionLocal()
        student = session.query(Student).filter_by(id=student_id).first()
        session.close()
        if student:
            return jsonify(student.serialize())
        else:
            return jsonify({"error": "Student not found"}), 404

    @app.route('/api/students', methods=['POST'])
    def add_student():
        """
        Add a new student.

        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Student
              required:
                - name
                - age
                - spec
              properties:
                name:
                  type: string
                  description: Name of the student.
                age:
                  type: integer
                  description: Age of the student.
                spec:
                  type: string
                  description: Specialization of the student.

        responses:
          201:
            description: Student added successfully.
          400:
            description: Incomplete data provided.
        """
        data = request.json
        name = data.get('name')
        age = data.get('age')
        spec = data.get('spec')
        if name and age and spec:
            new_student = Student(name=name, age=age, spec=spec)
            session = SessionLocal()
            session.add(new_student)
            session.commit()
            session.close()
            return jsonify({"message": "Student added successfully"}), 201
        else:
            return jsonify({"error": "Incomplete data"}), 400

    @app.route('/api/students/<int:student_id>', methods=['PUT'])
    def update_student(student_id):
        """
        Update a student by ID.

        ---
        parameters:
          - name: student_id
            in: path
            description: ID of the student to update
            required: true
            type: integer
          - name: body
            in: body
            required: true
            schema:
              $ref: '#/definitions/Student'
        responses:
          200:
            description: Student updated successfully.
          400:
            description: No data provided to update.
          404:
            description: Student not found.
        """
        data = request.json
        name = data.get('name')
        age = data.get('age')
        spec = data.get('spec')
        if name or age or spec:
            session = SessionLocal()
            student = session.query(Student).filter_by(id=student_id).first()
            if student:
                student.name = name if name else student.name
                student.age = age if age else student.age
                student.spec = spec if spec else student.spec
                session.commit()
                session.close()
                return jsonify({"message": "Student updated successfully"}), 200
            else:
                return jsonify({"error": "Student not found"}), 404
        else:
            return jsonify({"error": "No data provided to update"}), 400

    @app.route('/api/students/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        """
        Delete a student by ID.

        ---
        parameters:
          - name: student_id
            in: path
            description: ID of the student to delete
            required: true
            type: integer
        responses:
          200:
            description: Student deleted successfully.
          404:
            description: Student not found.
        """
        session = SessionLocal()
        student = session.query(Student).filter_by(id=student_id).first()
        if student:
            session.delete(student)
            session.commit()
            session.close()
            return jsonify({"message": "Student deleted successfully"}), 200
        else:
            session.close()
            return jsonify({"error": "Student not found"}), 404
