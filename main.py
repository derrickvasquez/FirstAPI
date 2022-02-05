# Importing modules
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Initializing app
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# creating a DB model
class PlayerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pos = db.Column(db.String(100), nullable=False)
    gp = db.Column(db.Integer, nullable=False)
    ab = db.Column(db.Integer, nullable=False)
    avg = db.Column(db.String(100), nullable=False)
    hr = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"PlayerStats(name ={name}, pos={pos}, gp={gp}, ab={ab}, avg={avg}, hr={hr})"


# Automatically parses
# Also setting mandatory arguments
player_put_args = reqparse.RequestParser()
player_put_args.add_argument("name", type=str, help="Name of Player is required", required=True)
player_put_args.add_argument("pos", type=str, help="Player's position is required", required=True)
player_put_args.add_argument("gp", type=int, help="Games Played is required", required=True)
player_put_args.add_argument("ab", type=int, help="At Bats is required", required=True)
player_put_args.add_argument("avg", type=str, help="Batting Average is required", required=True)
player_put_args.add_argument("hr", type=int, help="Home Runs is required", required=True)

player_update_args = reqparse.RequestParser()
player_update_args.add_argument("name", type=str, help="Name of Player is required",)
player_update_args.add_argument("pos", type=str, help="Player's position is required")
player_update_args.add_argument("gp", type=int, help="Games Played is required")
player_update_args.add_argument("ab", type=int, help="At Bats is required")
player_update_args.add_argument("avg", type=str, help="Batting Average is required")
player_update_args.add_argument("hr", type=int, help="Home Runs is required")



# creating a resource dictonary
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'pos': fields.String,
    'gp': fields.Integer,
    'ab': fields.Integer,
    'avg': fields.String,
    'hr': fields.Integer
}

# Defining a Resource
class PlayerStats(Resource):
    @marshal_with(resource_fields)
    def get(self, player_id):
        result = PlayerModel.query.filter_by(id=player_id).first()
        if not result:
            abort(404, message=" ** Could not find player **")
        return result

# Returning data + status code
    @marshal_with(resource_fields)
    def put(self, player_id):
        args = player_put_args.parse_args()
        result = PlayerModel.query.filter_by(id=player_id).first()
        if result:
            abort(409, message=' ** Player ID already exists **')

        player = PlayerModel(id=player_id, name = args['name'], pos = args['pos'], gp = args['gp'], ab = args['ab'], avg = args['avg'], hr = args['hr'])
        db.session.add(player)
        db.session.commit()
        return player, 201

# Update functionality
    @marshal_with(resource_fields)
    def patch(self, player_id):
        args = player_update_args.parse_args()
        result = PlayerModel.query.filter_by(id=player_id).first()
        if not result:
            abort(404, message ="** Cannot update player **")
        
        if args['name']:
            result.name = args['name']
        if args['pos']:
            result.pos = args['pos']
        if args['gp']:
            result.gp = args['gp']
        if args['ab']:
            result.ab = args['ab']
        if args['avg']:
            result.avg = args['avg']
        if args['hr']:
            result.hr = args['hr']
        
        db.session.commit()

        return result

# Deleting functionality
    def delete(self, player_id):
        no_player_id_abort(player_id)
        del players[player_id]
        return '', 204


api.add_resource(PlayerStats, "/playerstats/<int:player_id>")

if __name__ == "__main__":
    app.run(debug=True)

