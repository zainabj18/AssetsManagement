from app.db import get_db
from app.schemas import Project
from flask import Blueprint, jsonify, request
from psycopg import Error
from psycopg.rows import dict_row
from pydantic import ValidationError

bp = Blueprint("project", __name__, url_prefix="/project")


def get_projects(db):
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM projects;""")
            return cur.fetchall()


@bp.route("/", methods=["GET"])
def list():
    try:
        db = get_db()
        projects = get_projects(db)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return jsonify({"msg": "projects", "data": projects})


@bp.route("/new", methods=["POST"])
def create():
    try:
        try:
            project = Project(**request.json)
        except ValidationError as e:
            return (
                jsonify(
                    {
                        "msg": "Data provided is invalid",
                        "data": e.errors(),
                        "error": "Failed to create asset from the data provided",
                    }
                ),
                400,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": None,
                    "error": "Failed to create asset from the data provided",
                }
            ),
            400,
        )
        import { useEffect, useState } from 'react';
import { Box, Divider, Heading, Text } from '@chakra-ui/react';

function CommentDisplay({ assetId }) {
  const [comments, setComments] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(`/api/assets/${assetId}/comments`);
        if (!response.ok) {
          throw new Error(`Failed to retrieve comments for asset ${assetId}`);
        }
        const data = await response.json();
        setComments(data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchComments();
  }, [assetId]);

  if (error) {
    return <Box>{error}</Box>;
  }

  return (
    <Box mt={4}>
      <Heading size="md">{comments.length} Comments</Heading>
      {comments.map((comment) => (
        <Box key={comment.id} mt={4}>
          <Text fontWeight="bold">{comment.username}</Text>
          <Text>{comment.content}</Text>
          <Text fontSize="sm">{new Date(comment.timestamp).toLocaleString()}</Text>
          <Divider my={2} />
        </Box>
      ))}
    </Box>
  );
}

export default CommentDisplay;

    print(project)
    db = get_db()
    db_project = project.dict()
    with db.connection() as conn:
        conn.execute(
            """INSERT INTO projects (name,description)VALUES (%(name)s,%(description)s);""",
            db_project,
        )

    return jsonify({"msg": "The user have created a new project"}), 200
